# Task Processing System Component Diagrams

## 1. Client Interaction Flow
```mermaid
sequenceDiagram
    participant Client
    participant Flask
    participant RabbitMQ
    participant Worker
    participant Redis

    Client->>Flask: Submit Task (POST /api/tasks)
    Flask->>RabbitMQ: Queue Task
    RabbitMQ->>Worker: Process Task
    Worker->>Redis: Store Result
    Client->>Flask: Check Status (GET /api/tasks/<id>)
    Flask->>Redis: Query Result
    Redis-->>Flask: Return Status
    Flask-->>Client: Return Status
```

## 2. Priority Queue System
```mermaid
graph LR
    subgraph Task Submission
        Task[New Task]
    end

    subgraph Priority Router
        Router[Priority Router]
    end

    subgraph Queues
        High[High Priority Queue]
        Normal[Normal Priority Queue]
        Low[Low Priority Queue]
    end

    Task -->|Submit| Router
    Router -->|Priority: High| High
    Router -->|Priority: Normal| Normal
    Router -->|Priority: Low| Low

    style Task fill:#f9f,stroke:#333,stroke-width:2px
    style Router fill:#bbf,stroke:#333,stroke-width:2px
    style High fill:#fbb,stroke:#333,stroke-width:2px
    style Normal fill:#bfb,stroke:#333,stroke-width:2px
    style Low fill:#fbf,stroke:#333,stroke-width:2px
```

## 3. Worker Processing Flow
```mermaid
stateDiagram-v2
    [*] --> Received: Task Arrives
    Received --> Processing: Start Processing
    Processing --> Success: Task Complete
    Processing --> Failed: Error Occurs
    Failed --> Retrying: Retry Logic
    Retrying --> Processing: Retry Attempt
    Success --> [*]: Store Result
    Failed --> [*]: Max Retries Reached
```

## 4. Task Types and Workers
```mermaid
graph TB
    subgraph Task Types
        Data[Data Processing Task]
        Email[Email Task]
        File[File Processing Task]
    end

    subgraph Workers
        DataW[Data Worker]
        EmailW[Email Worker]
        FileW[File Worker]
    end

    Data -->|Process| DataW
    Email -->|Send| EmailW
    File -->|Handle| FileW

    style Data fill:#f9f,stroke:#333,stroke-width:2px
    style Email fill:#bbf,stroke:#333,stroke-width:2px
    style File fill:#bfb,stroke:#333,stroke-width:2px
    style DataW fill:#fbb,stroke:#333,stroke-width:2px
    style EmailW fill:#fbf,stroke:#333,stroke-width:2px
    style FileW fill:#bff,stroke:#333,stroke-width:2px
```

## 5. Monitoring System
```mermaid
graph LR
    subgraph Workers
        W1[Worker 1]
        W2[Worker 2]
        W3[Worker 3]
    end

    subgraph Monitoring
        Flower[Flower Dashboard]
        Metrics[Task Metrics]
        Status[Worker Status]
    end

    W1 -->|Report| Flower
    W2 -->|Report| Flower
    W3 -->|Report| Flower
    Flower -->|Display| Metrics
    Flower -->|Display| Status

    style Flower fill:#f9f,stroke:#333,stroke-width:2px
    style Metrics fill:#bbf,stroke:#333,stroke-width:2px
    style Status fill:#bfb,stroke:#333,stroke-width:2px
```

## 6. Error Handling Flow
```mermaid
graph TD
    subgraph Error Handling
        Error[Error Occurs]
        Retry[Retry Logic]
        Backoff[Exponential Backoff]
        MaxRetries[Max Retries Check]
        Log[Error Logging]
    end

    Error -->|Trigger| Retry
    Retry -->|Calculate| Backoff
    Backoff -->|Check| MaxRetries
    MaxRetries -->|Continue| Retry
    MaxRetries -->|Stop| Log
    Error -->|Record| Log

    style Error fill:#f9f,stroke:#333,stroke-width:2px
    style Retry fill:#bbf,stroke:#333,stroke-width:2px
    style Backoff fill:#bfb,stroke:#333,stroke-width:2px
    style MaxRetries fill:#fbb,stroke:#333,stroke-width:2px
    style Log fill:#fbf,stroke:#333,stroke-width:2px
``` 