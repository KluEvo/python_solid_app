# 🎤 Presentation Script — Book Management Application

---

## Slide 1 — Title & Framing (30 sec)

**[SLIDE]**

> “This project is a Book Management Application written in Python, designed around SOLID principles and a layered architecture.”

> “The goal wasn’t just to build features—it was to build something that’s clean, maintainable, and easy to extend.”

> “I’ll walk through the system from both an **architect’s perspective** and a **user’s perspective**.”

> “So first, I’ll start with the architecture.”

---

## Slide 2 — High-Level Architecture (45 sec)

**[SLIDE – diagram visible]**

> “At a high level, the application is split into four layers.”

> “This separation is intentional. Each layer has one clear responsibility, and layers only talk *down*, never sideways.”

> “From top to bottom, we have:
>
> * the Application layer (the REPL),
> * the Service layer,
> * the Repository layer,
> * and the Domain layer.”

> “This structure makes it very obvious *where code belongs* and *where it does not belong*.”

> “I’ll briefly explain what each layer does, then we’ll see it in action.”

---

## Slide 3 — Layer Responsibilities (60 sec)

**[SLIDE]**

> “Starting from the bottom: the **Domain layer** defines what a book *is*.”

> “This is where the core entities live—like the Book object—and where validation and business rules exist.”

> “The key idea is that the domain knows **nothing** about the UI, databases, or analytics.”

---

> “Above that is the **Repository layer**.”

> “Its only job is persistence: saving and loading books.”

> “Right now it uses JSON, but because everything depends on interfaces, this could be swapped for SQL later without touching the service or domain layers.”

---

> “Next is the **Service layer**, which is really the brain of the application.”

> “This is where workflows live—things like checking out a book, checking it back in, enforcing availability rules, and coordinating between domain objects and repositories.”

---

> “Finally, the **Application layer** is just the REPL.”

> “It handles user input, prints output, and delegates everything else.”

> “No business logic, no data access—just orchestration.”

---

## Transition to Demo — User Perspective

> “With that context, let’s look at the system from a **user’s point of view**.”

---

## Demo 1 — Basic User Flow (60 sec)

**[DEMO – REPL]**

> “From the user’s perspective, this is a simple command-driven application.”

> “I can find a book by name, add or delete a new book, and update the data for a book.”

*(Demo: find book, add a book, show it appears)*

> “What’s important architecturally is that the REPL isn’t doing any real work.”

> “Every command maps to a service call, and the service decides what happens next.”

---

## Slide 4 — SOLID Principles in Action (45 sec)

**[SLIDE]**

> “This layered approach directly supports SOLID principles.”

> “For example:
>
> * Following **Single Responsibility**: each layer does one thing
> * For **Dependency Inversion** services depend on repository interfaces, not implementations
> * Meanwhile, **Open/Closed** is cheaved as adding a new storage backend doesn’t require rewriting logic”
> * Similarly, the use of protocols allow us to switch repository implementations without affecting the functionality of the service 

---

## Demo 2 — Workflow Feature (45 sec)

**[DEMO – check-out / check-in]**

> “A good example of that is checking out a book.”

*(Demo: check out a book)*

> “This triggers a workflow in the service layer.”

> “The service enforces rules like availability, updates the domain object, and persists the change through the repository.”

> “From the REPL, this looks simple—but behind the scenes, responsibilities are cleanly separated.”

---

## Slide 5 — Analytics & Data Science Integration (60 sec)

**[SLIDE]**

> “Beyond core functionality, this project also includes an analytics component.”

> “Instead of treating analytics as a separate project, the same data is reused using pandas and NumPy.”

> “Pandas allows us to clean and transform book data into DataFrames,”

> “While, NumPy supports numerical operations, and Matplotlib lets us visualize trends in a meaningful way.”

---

> “Examples include:
>
> * genre popularity,
> * ratings by genre using a Bayesian average,
> * price versus rating correlations,
> * publication trends over time,
> * and availability status.”

> “This turns the application into both a management system *and* a decision-support tool.”

---

## Slide 6 — Why This Design Works (30–45 sec)

**[SLIDE]**

> “To wrap up, this project focuses on how everything fits together cleanly.”

> “Each layer has a clear purpose:
>
> * Domain defines the business
> * Services define workflows
> * Repositories handle persistence
> * The REPL handles interaction”

> “This makes the system easier to test, easier to extend, and easier to reason about.”

---

## Closing (15 sec)

> “Overall, this project demonstrates how SOLID principles and layered architecture scale from core application logic all the way to analytics.”

> “Thanks—happy to answer questions.”
