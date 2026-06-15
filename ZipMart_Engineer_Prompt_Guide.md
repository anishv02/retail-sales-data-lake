# ⚡ ZipMart — Engineer Prompt Guide
### Everything your software engineer friend needs to build this with Claude Opus on Antigravity

---

## 🧭 WHAT ARE YOU BUILDING?

A **Blinkit-style quick commerce app for Tier 3 towns in India** called **ZipMart**. The core idea: partner with existing local kirana stores (not build dark stores), serve customers in towns with 20k-1 lakh population, and optimize for low internet, cash-first, Hindi-speaking users.

---

## 🛠️ WHAT IS ANTIGRAVITY?

Antigravity is Google's high-performance inference environment that runs Claude Opus. Your engineer will:
1. Open Google Cloud Console → Vertex AI
2. Access Claude Opus via Model Garden or Antigravity API
3. Use it exactly like the Anthropic API but through Google's infrastructure

**API call format is identical to Anthropic's — just the endpoint URL changes.**

---

## 📦 WHAT TO HAND YOUR ENGINEER

Give your engineer this file and the `ZipMart_Technical_Documentation.docx`. Then tell them to use the prompts below in Claude Opus.

---

## 🔧 SETUP PROMPT (Send This First)

> You are a senior full-stack engineer helping build **ZipMart**, a quick commerce app for Tier 3 Indian towns (like Blinkit but for small cities). 
>
> **Tech stack:**
> - Backend: Node.js 20 + Express 4 + PostgreSQL 15 + Redis 7
> - Customer App: React Native 0.73 + Expo
> - State: Redux Toolkit + React Query
> - Payments: Razorpay
> - Maps: Google Maps API
> - Auth: Firebase OTP
> - Storage: AWS S3
> - Realtime: Socket.io
>
> **Key constraints:**
> - Must work on 2G/3G (minimize API payload sizes)
> - Support Hindi voice search
> - Cash on Delivery is primary payment
> - Target Android-first, low-end devices (2GB RAM)
>
> I will give you tasks one by one. For each task, write production-ready code with proper error handling. Use ES modules. Follow REST conventions.

---

## 🏗️ BACKEND PROMPTS (In Order)

### 1. Project Structure
```
Create a Node.js + Express backend folder structure for ZipMart with these services:
- auth (OTP-based login)
- users (profile, addresses)
- stores (kirana store management)
- products (catalog)
- orders (order lifecycle)
- delivery (partner management + routing)
- payments (Razorpay integration)
- notifications (FCM + SMS)

Include: app.js, server.js, .env.example, and a base router. Use ES modules.
```

### 2. Database Schema
```
Write PostgreSQL migration files for ZipMart with these tables:
users, stores, store_owners, products, categories, orders, order_items, 
delivery_partners, deliveries, payments, zones, promotions, reviews

Include: proper indexes for lat/lng queries (PostGIS), foreign keys, 
created_at/updated_at timestamps. Use snake_case naming.
```

### 3. Auth Service
```
Build the auth service for ZipMart:
- POST /auth/send-otp → sends OTP via Firebase Auth (phone number)
- POST /auth/verify-otp → verifies OTP, creates user if new, returns JWT
- Middleware: authenticateUser (validates JWT, attaches user to req)

Use Firebase Admin SDK. JWT secret from env. Handle: invalid OTP, expired OTP, 
rate limiting (max 3 OTP requests per hour per number).
```

### 4. Store & Product APIs
```
Build these Express routes for ZipMart:
- GET /stores/nearby?lat=&lng=&radius= → returns stores within radius using PostGIS
- GET /stores/:id → store details with ratings
- GET /stores/:id/products?category=&page= → paginated product list
- GET /products/search?q=&store_id=&lang= → text search (support Hindi transliteration)
- POST /stores (protected: admin) → onboard a new kirana store

Each should return minimal JSON (for low-bandwidth). Include proper validation.
```

### 5. Order Service
```
Build the complete order flow for ZipMart:
- POST /orders/create → validate cart, check stock, create order, deduct inventory
- GET /orders/:id → order details + current status
- PATCH /orders/:id/cancel → customer cancels (only if pending)
- PATCH /orders/:id/status (store partner) → accept, preparing, ready
- GET /orders/:id/track → current delivery partner location + ETA

Use database transactions for inventory. Emit Socket.io events on status changes.
Status flow: PENDING → ACCEPTED → PREPARING → READY → PICKED_UP → DELIVERED
```

### 6. Payment Integration
```
Integrate Razorpay into ZipMart:
- POST /payments/create-order → create Razorpay order
- POST /payments/verify → verify payment signature
- POST /payments/webhook → handle payment events (use raw body parser)
- Support: UPI, Cards, Wallets, and COD (COD just marks order as cash_on_delivery)

Store payment records in DB. On success: confirm order. On failure: restore inventory.
```

### 7. Delivery Assignment
```
Build the delivery assignment system for ZipMart:
- When an order is marked READY by the store, automatically find the nearest 
  available delivery partner within 3km using PostGIS ST_Distance
- POST /delivery/accept/:order_id → delivery partner accepts
- PATCH /delivery/:id/picked → mark picked up (generate 4-digit OTP for customer)
- PATCH /delivery/:id/complete → verify OTP, mark delivered, trigger payout record

Delivery partner sends GPS every 30 seconds via PATCH /delivery/location
Broadcast location to customer via Socket.io room order_{id}
```

---

## 📱 REACT NATIVE PROMPTS

### 8. Project Setup
```
Create a React Native 0.73 + Expo project for ZipMart customer app:
- Navigation: React Navigation 6 (bottom tabs + stack)
- Tabs: Home, Search, Orders, Profile
- Auth flow: Splash → OTP Login → Main App
- State: Redux Toolkit store with slices for: auth, cart, orders, location
- API layer: Axios instance with JWT interceptor and retry logic

Include folder structure: screens/, components/, store/, api/, utils/, hooks/
```

### 9. Home Screen
```
Build the ZipMart Home Screen in React Native:
- Header with location picker and search bar
- Horizontal scrollable category pills (Groceries, Dairy, Snacks, Vegetables...)
- "Stores near you" section with store cards (name, distance, delivery time, min order)
- "Order Again" section if user has past orders
- Sale banner (if any active promotions)
- Pull to refresh

Use placeholder data for now. Optimize for low-end Android (avoid heavy animations).
Style: Indian quick commerce feel — orange and white, clean, big tap targets.
```

### 10. Voice Search
```
Build a voice search component for ZipMart:
- Mic button on search bar
- Record using expo-av or react-native-voice
- Send audio to Google Speech-to-Text API (language: hi-IN, with fallback to en-IN)
- Show transcript, search products with result
- Handle: no mic permission, network error, empty result

The component should look like a floating modal with animated waveform while listening.
```

### 11. Cart & Checkout
```
Build the Cart and Checkout flow for ZipMart:
- Cart screen: list items with +/- qty controls, item total, delivery fee, grand total
- Coupon code input field
- Checkout screen: 
  - Address selector (saved addresses or add new with map pin)
  - Payment method: UPI / COD (show COD prominently)
  - Order summary
  - Place Order button → call POST /orders/create
  
Show estimated delivery time (25-35 min). Cart should persist in Redux + AsyncStorage.
```

### 12. Live Order Tracking
```
Build the Order Tracking screen for ZipMart:
- Progress stepper: Order Placed → Store Accepted → Preparing → Out for Delivery → Delivered
- Live map showing delivery partner location (update every 30s via Socket.io)
- Customer's address marked on map
- Estimated time remaining
- Delivery partner name, rating, and phone call button
- OTP display (for COD orders, show the 4-digit OTP delivery partner will verify)

Use react-native-maps. Connect to Socket.io room order_{orderId}.
```

---

## 🏪 STORE PARTNER APP PROMPTS

### 13. Store Partner App
```
Build the Store Partner App for ZipMart in React Native:
Screen 1 - Order Queue:
- List of PENDING orders with timer (accept within 2 minutes or auto-reject)
- Each card: customer name, items count, total, accept/reject buttons
- Sound notification + vibration on new order

Screen 2 - Active Orders:
- Orders being prepared, with "Mark as Ready" button

Screen 3 - Inventory:
- Product list with quick stock toggle (in stock / out of stock)
- Edit price button

Connect to Socket.io for real-time new order events. This is a separate RN app 
or same app with role-based routing.
```

---

## 🛵 DELIVERY PARTNER APP PROMPTS

### 14. Delivery Partner App
```
Build the Delivery Partner App for ZipMart in React Native:
- Online/Offline toggle (big, prominent)
- When online: show nearby available orders
- Active delivery screen: 
  - Navigate to store (Google Maps deeplink)
  - "Picked Up" button → mark order picked
  - Navigate to customer
  - "Delivered" button → enter OTP to confirm
- Earnings today / this week

Send GPS location to backend every 30 seconds when online and on an active delivery.
Optimize heavily — this app will run on ₹6,000 Android phones.
```

---

## 🖥️ ADMIN PANEL PROMPTS

### 15. Admin Dashboard
```
Build an admin dashboard for ZipMart using React.js + Tailwind CSS:
- Live stats cards: Active Orders, Deliveries in Progress, Online Partners, GMV Today
- Orders table with filters (status, city, store) and manual override actions
- Store management: list, approve/reject applications, toggle active status
- Delivery partner management: list, verify, deactivate
- Promotions: create coupon codes with rules

Use React Query for data fetching. Charts using Recharts.
```

---

## 🔒 SECURITY & PERFORMANCE PROMPTS

### 16. Security Hardening
```
Review and harden the ZipMart backend for production:
- Add rate limiting (express-rate-limit) to all public endpoints
- Add Helmet.js security headers
- Validate all inputs with Joi or Zod
- Prevent SQL injection (ensure all queries use parameterized inputs)
- Add request size limits
- Secure the Razorpay webhook with signature verification
- Review JWT implementation for expiry and refresh token flow

List any security issues you find in the existing patterns and fix them.
```

### 17. Low-Bandwidth Optimization
```
Optimize ZipMart APIs for 2G/3G users in Tier 3 India:
- Compress all API responses with gzip (compression middleware)
- Paginate all list endpoints (max 10 items per page)
- Add response caching with Redis (products: 5min TTL, stores: 2min, user: no cache)
- Add ETag support for product catalog
- Reduce product image URLs to serve via Cloudflare with quality params
- Review and trim all JSON responses to remove unused fields

Show before/after payload sizes for the top 3 heaviest endpoints.
```

---

## 🧪 TESTING PROMPTS

### 18. Unit Tests
```
Write Jest unit tests for ZipMart's order service covering:
- createOrder: valid cart, out of stock items, invalid store, promo code validation
- cancelOrder: within cancellation window, after pickup (should fail)
- calculateDeliveryFee: distance-based fee calculation
- assignDeliveryPartner: no partners available, multiple partners (pick nearest)

Use mocked database calls. Aim for 80%+ coverage of the order service.
```

---

## 📋 PROMPTING TIPS FOR YOUR ENGINEER

1. **Always start with the Setup Prompt** — sets context for the whole session
2. **One module at a time** — don't ask Claude to build everything in one prompt
3. **Paste existing code** when asking for changes: *"Here is my current orders.js, add the cancellation endpoint"*
4. **Ask for trade-offs** when making architecture decisions
5. **Review every output** — Claude writes good code but you must read it before running
6. **Ask Claude to explain** any part you don't understand: *"Explain what the Socket.io room logic is doing here"*

---

## 🚀 BUILD ORDER (Recommended Sequence)

```
Week 1:  DB Schema + Auth + Project Setup
Week 2:  Store/Product APIs + Order Service
Week 3:  Payment Integration + Delivery Assignment  
Week 4:  Customer App (Home + Cart + Checkout)
Week 5:  Customer App (Tracking + Profile + Voice)
Week 6:  Store Partner App
Week 7:  Delivery Partner App
Week 8:  Admin Panel + Security + Tests
Week 9:  Bug fixes, optimization, staging deploy
Week 10: Beta launch in 1 city 🚀
```

---

*ZipMart | Built with AI-Assisted Development | Claude Opus via Antigravity | 2025*
