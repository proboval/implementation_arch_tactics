# Architectural Tactics

Architectural tactics are the core mechanism through which architects translate quality attribute requirements into concrete design decisions. While the previous chapter established *what* maintainability means and *how* to measure it, this chapter addresses the more fundamental question: *what specific design decisions improve maintainability, and how can they be systematically applied?* This is the central chapter of the study guide because the thesis proposes automating the implementation of these tactics using large language models.

## 4.1 What Are Architectural Tactics?

### Definition

An architectural tactic is formally defined as:

> "A design decision that influences the achievement of a quality attribute response." [@bass2021software]

More concretely, a tactic is a targeted architectural intervention that addresses a single quality attribute concern. If a system needs to be modifiable, there are specific, named design decisions -- like encapsulating implementation behind interfaces or splitting large modules into focused components -- that an architect can apply. These named decisions are tactics.

Kim et al. elaborate on this definition:

> "An architectural tactic is a fine-grained reusable architectural building block that provides an architectural solution built from experience to help to achieve a quality attribute." [@kim2009qualitydriven]

The word "fine-grained" is critical. Tactics are deliberately small and focused. Each tactic targets a single quality attribute response, without worrying about side effects on other quality attributes. This is what distinguishes them from patterns, which are larger, more complex structures that inherently embed tradeoff decisions.

### The Design Hierarchy: Style, Pattern, Tactic, Technique

To understand tactics properly, you must understand where they sit in the hierarchy of architectural design concepts. From most abstract to most concrete:

| Level | Concept | Scope | Example | Quality Scope |
|-------|---------|-------|---------|---------------|
| **Style** | Overall structural organization | System-wide | Layered, Microservices, Event-Driven, Pipe-and-Filter | Multiple quality attributes simultaneously |
| **Pattern** | Recurring solution template | Subsystem or component group | MVC, Repository, Observer, Broker | Multiple quality attributes with built-in tradeoffs |
| **Tactic** | Targeted quality attribute decision | Component or interface level | Split Module, Use an Intermediary, Publish-Subscribe | **Single quality attribute** |
| **Design Technique** | Code-level implementation | Class or method level | Factory Method, Dependency Injection, Strategy Pattern | Implementation of a tactic |

Bass et al. explain the relationship between tactics and patterns:

> "Architectural tactics are 'building blocks' from which architecture patterns are created; patterns package tactics." [@bass2021software]

This means that when you look inside any architectural pattern, you find a collection of tactics working together. The MVC pattern, for example, packages the "Split Module" tactic (separating model, view, and controller into distinct components), the "Use Encapsulation" tactic (each component hides its internals), and the "Restrict Dependencies" tactic (the view cannot directly modify the model without going through the controller). Understanding this decomposition is what allows us to reason about *which specific aspect* of a pattern produces *which specific quality attribute benefit*.

### The Quality Attribute Scenario Model

Tactics do not exist in a vacuum. They are applied in response to specific quality attribute scenarios. Bass et al. define a six-part scenario model that structures how we think about quality requirements and the tactics that address them [@bass2021software]:

| Part | Description | Example (Modifiability) |
|------|-------------|------------------------|
| **Source of stimulus** | The entity that causes the change | A developer on the team |
| **Stimulus** | The change or event that must be accommodated | Wants to replace the payment gateway from Stripe to PayPal |
| **Environment** | The conditions under which the stimulus occurs | Design time (the system is not running) |
| **Artifact** | The part of the system affected | The payment processing module |
| **Response** | What the system (or development process) does | The change is made with no side effects on other modules |
| **Response measure** | How we know the response was satisfactory | Completed in less than 3 person-hours, affecting at most 2 modules, all tests pass |

The tactic is the design decision that enables the desired response. In this example, if the payment module uses the "Use an Intermediary" tactic (a payment gateway facade), then replacing the underlying gateway implementation requires changing only the facade's internal wiring -- achieving the response measure of affecting at most 2 modules.

Without the tactic, the payment gateway might be referenced directly in 15 modules across the codebase, and replacing it would require modifying all 15 -- violating the response measure and indicating a modifiability deficiency.

### Quality Attribute Tactics Taxonomy

Bass et al. define tactics for seven quality attributes [@bass2021software]:

| Quality Attribute | Tactic Categories | Example Tactics |
|-------------------|------------------|-----------------|
| **Availability** | Detect Faults, Recover from Faults, Prevent Faults | Heartbeat, Voting, Active Redundancy, Checkpoint/Rollback |
| **Interoperability** | Locate Services, Manage Interfaces | Discover Service, Orchestrate, Tailor Interface |
| **Modifiability** | Increase Cohesion, Reduce Coupling, Defer Binding | Split Module, Use an Intermediary, Publish-Subscribe |
| **Performance** | Control Resource Demand, Manage Resources | Reduce Overhead, Manage Sampling Rate, Introduce Concurrency |
| **Security** | Resist Attacks, Detect Attacks, Recover from Attacks | Authenticate Users, Authorize Users, Encrypt Data |
| **Testability** | Observe/Control System State | Record/Playback, Abstract Data Sources, Sandbox |
| **Usability** | User Initiative, System Initiative | Cancel, Undo, Task Model, User Model |

This thesis focuses exclusively on **modifiability tactics** because they (a) directly target ISO 25010 maintainability sub-characteristics, (b) are implementable through source code transformation, and (c) produce measurable changes in static analysis metrics.

## 4.2 The Modifiability Tactics Catalog

Bass, Clements, and Kazman define 15 modifiability tactics organized into three categories based on the mechanism they use to improve modifiability [@bass2021software]. The categories correspond to three fundamental strategies:

1. **Increase Cohesion** -- ensure that things that change together are located together
2. **Reduce Coupling** -- ensure that changes in one module do not propagate to others
3. **Defer Binding Time** -- delay decisions so they can be changed without modifying code

For each tactic below, we provide: the definition, how it works mechanically, which ISO 25010 sub-characteristic it targets, and a concrete Python code example showing the transformation.

### Category 1: Increase Cohesion (5 Tactics)

The cohesion tactics ensure that each module has a single, well-defined purpose. When cohesion is high, a change in requirements typically affects only one module because related responsibilities are co-located.

#### Tactic 1: Split Module

**Definition:** Break a module that has multiple responsibilities into smaller, focused modules, each with a single responsibility.

**How it works:** Identify distinct responsibilities within a module (e.g., data validation, business logic, persistence). Extract each responsibility into its own module with a clear interface. The original module may become a thin coordinator or may be eliminated entirely.

**ISO 25010 target:** Modularity, Modifiability

**Example:**

Before -- a monolithic user service:

```python
# user_service.py -- handles everything user-related
class UserService:
    def validate_email(self, email):
        import re
        return bool(re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email))

    def hash_password(self, password):
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def save_user(self, user_data):
        # Direct database interaction
        conn = get_db_connection()
        conn.execute("INSERT INTO users ...", user_data)
        conn.commit()

    def send_welcome_email(self, email):
        import smtplib
        server = smtplib.SMTP('smtp.example.com')
        server.send_message(...)

    def register_user(self, name, email, password):
        if not self.validate_email(email):
            raise ValueError("Invalid email")
        hashed = self.hash_password(password)
        self.save_user({"name": name, "email": email, "password": hashed})
        self.send_welcome_email(email)
```

After -- split into focused modules:

```python
# validation.py
class UserValidator:
    def validate_email(self, email: str) -> bool:
        import re
        return bool(re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email))

# security.py
class PasswordService:
    def hash_password(self, password: str) -> str:
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

# user_repository.py
class UserRepository:
    def save(self, user_data: dict) -> None:
        conn = get_db_connection()
        conn.execute("INSERT INTO users ...", user_data)
        conn.commit()

# notification.py
class EmailNotificationService:
    def send_welcome_email(self, email: str) -> None:
        import smtplib
        server = smtplib.SMTP('smtp.example.com')
        server.send_message(...)

# user_service.py -- now a thin coordinator
class UserService:
    def __init__(self, validator, password_svc, repo, notifier):
        self.validator = validator
        self.password_svc = password_svc
        self.repo = repo
        self.notifier = notifier

    def register_user(self, name: str, email: str, password: str):
        if not self.validator.validate_email(email):
            raise ValueError("Invalid email")
        hashed = self.password_svc.hash_password(password)
        self.repo.save({"name": name, "email": email, "password": hashed})
        self.notifier.send_welcome_email(email)
```

The transformation reduces the cyclomatic complexity of each individual module, improves testability (each module can be tested independently with mock dependencies), and increases modularity (changing the email service does not require touching the password hashing logic).

#### Tactic 2: Abstract Common Services

**Definition:** Identify common functionality used across multiple modules and extract it into a shared service, base class, or utility module.

**How it works:** When two or more modules contain duplicated or near-duplicated logic, extract that logic into a common module and have both modules depend on it. This eliminates duplication and creates a single point of change.

**ISO 25010 target:** Modularity, Reusability

**Example:**

Before -- duplicated logging and error handling in two services:

```python
# order_service.py
class OrderService:
    def create_order(self, data):
        try:
            # business logic...
            import logging
            logging.getLogger("orders").info(f"Order created: {data['id']}")
            return {"status": "success", "data": result}
        except Exception as e:
            import logging
            logging.getLogger("orders").error(f"Order failed: {e}")
            return {"status": "error", "message": str(e)}

# inventory_service.py
class InventoryService:
    def update_stock(self, data):
        try:
            # business logic...
            import logging
            logging.getLogger("inventory").info(f"Stock updated: {data['sku']}")
            return {"status": "success", "data": result}
        except Exception as e:
            import logging
            logging.getLogger("inventory").error(f"Update failed: {e}")
            return {"status": "error", "message": str(e)}
```

After -- common service extracted:

```python
# common/service_base.py
import logging
from typing import Any, Callable

class ServiceBase:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)

    def execute(self, operation: Callable, success_msg: str,
                *args, **kwargs) -> dict:
        try:
            result = operation(*args, **kwargs)
            self.logger.info(success_msg)
            return {"status": "success", "data": result}
        except Exception as e:
            self.logger.error(f"Operation failed: {e}")
            return {"status": "error", "message": str(e)}

# order_service.py
class OrderService(ServiceBase):
    def __init__(self):
        super().__init__("orders")

    def create_order(self, data):
        return self.execute(
            self._do_create_order,
            f"Order created: {data['id']}",
            data
        )

    def _do_create_order(self, data):
        # pure business logic
        ...
```

This transformation eliminates code duplication (Visser's Guideline 3: Write Code Once), creates a single point of change for logging/error handling behavior, and improves reusability by making the common pattern available to all future services.

#### Tactic 3: Increase Semantic Coherence

**Definition:** Ensure that all responsibilities within a module are semantically related -- that they serve a single, unified purpose.

**How it works:** Analyze the responsibilities of each module and identify responsibilities that are semantically unrelated to the module's primary purpose. Move those responsibilities to more appropriate modules. This differs from "Split Module" in that it focuses on *reassigning* misplaced responsibilities rather than decomposing a module entirely.

**ISO 25010 target:** Modularity, Analysability

**Example:**

Before -- a `UserProfile` class that also manages authentication:

```python
# user_profile.py
class UserProfile:
    def get_display_name(self, user_id):
        ...  # Profile concern

    def update_avatar(self, user_id, image):
        ...  # Profile concern

    def verify_password(self, user_id, password):
        ...  # Authentication concern -- wrong module!

    def generate_api_token(self, user_id):
        ...  # Authentication concern -- wrong module!

    def get_profile_stats(self, user_id):
        ...  # Profile concern
```

After -- coherent modules:

```python
# user_profile.py -- only profile responsibilities
class UserProfile:
    def get_display_name(self, user_id):
        ...
    def update_avatar(self, user_id, image):
        ...
    def get_profile_stats(self, user_id):
        ...

# authentication.py -- only auth responsibilities
class AuthenticationService:
    def verify_password(self, user_id, password):
        ...
    def generate_api_token(self, user_id):
        ...
```

#### Tactic 4: Encapsulate

**Definition:** Group related elements (data and the operations that manipulate that data) and expose only a well-defined interface to the rest of the system.

**How it works:** Identify data that is accessed directly by external modules. Wrap that data in a class or module with a controlled API. External modules interact only through the API, not with the underlying data structures or implementation.

**ISO 25010 target:** Modularity, Modifiability

**Example:**

Before -- direct access to data structures:

```python
# Callers directly access and manipulate the internal dict
order = {"items": [], "total": 0, "status": "pending"}
order["items"].append({"sku": "ABC", "price": 29.99, "qty": 2})
order["total"] = sum(i["price"] * i["qty"] for i in order["items"])
order["status"] = "confirmed"
```

After -- encapsulated with controlled interface:

```python
class Order:
    def __init__(self):
        self._items = []
        self._status = "pending"

    def add_item(self, sku: str, price: float, qty: int) -> None:
        self._items.append({"sku": sku, "price": price, "qty": qty})

    @property
    def total(self) -> float:
        return sum(i["price"] * i["qty"] for i in self._items)

    def confirm(self) -> None:
        if not self._items:
            raise ValueError("Cannot confirm empty order")
        self._status = "confirmed"

    @property
    def status(self) -> str:
        return self._status
```

Now the internal representation (a list of dicts) can be changed to a database-backed structure, a dataclass, or any other format without affecting any module that uses `Order`. The encapsulation boundary protects external modules from internal change.

#### Tactic 5: Restrict Dependencies

**Definition:** Limit which modules are permitted to depend on which other modules, enforcing architectural rules that prevent uncontrolled coupling.

**How it works:** Define explicit dependency rules (e.g., "presentation modules may not import data access modules directly; they must go through service modules"). Enforce these rules through conventions, linting rules, or architectural constraints. Remove or redirect any violating dependencies.

**ISO 25010 target:** Modularity, Testability

**Example:**

Before -- uncontrolled imports creating a tangled dependency graph:

```python
# views/dashboard.py -- presentation layer importing directly from data layer
from database.queries import get_user_stats, get_order_history
from database.connection import get_raw_connection
from utils.formatters import format_currency
from services.cache import CacheManager
```

After -- dependencies restricted to follow layering rules:

```python
# views/dashboard.py -- presentation layer imports only from service layer
from services.dashboard_service import DashboardService

class DashboardView:
    def __init__(self, dashboard_service: DashboardService):
        self.service = dashboard_service

    def render(self, user_id: str):
        stats = self.service.get_user_dashboard(user_id)
        return self.template.render(stats=stats)
```

```python
# services/dashboard_service.py -- service layer mediates access
from repositories.user_repository import UserRepository
from repositories.order_repository import OrderRepository

class DashboardService:
    def __init__(self, user_repo: UserRepository, order_repo: OrderRepository):
        self.user_repo = user_repo
        self.order_repo = order_repo

    def get_user_dashboard(self, user_id: str) -> dict:
        stats = self.user_repo.get_stats(user_id)
        orders = self.order_repo.get_recent(user_id)
        return {"stats": stats, "orders": orders}
```

### Category 2: Reduce Coupling (4 Tactics)

Coupling tactics prevent changes from propagating across module boundaries. When coupling is low, modifying one module does not require modifying others -- the change is contained.

#### Tactic 6: Use Encapsulation

**Definition:** Hide a module's internal implementation behind a stable public interface, so that changes to the implementation do not affect dependent modules.

**How it works:** Define a clear boundary between a module's interface (what it promises to do) and its implementation (how it does it). External modules depend only on the interface, never on implementation details. In Python, this often involves using abstract base classes, protocols, or well-defined public APIs.

**ISO 25010 target:** Modularity, Modifiability

**Example:**

Before -- callers depend on a specific implementation:

```python
# Multiple modules directly use the Redis client
import redis

class OrderCache:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379)

    def get_order(self, order_id):
        data = self.client.get(f"order:{order_id}")
        return json.loads(data) if data else None
```

After -- implementation hidden behind an interface:

```python
# cache/interface.py
from abc import ABC, abstractmethod

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> dict | None: ...

    @abstractmethod
    def set(self, key: str, value: dict, ttl: int = 3600) -> None: ...

# cache/redis_cache.py
class RedisCache(CacheInterface):
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port)

    def get(self, key: str) -> dict | None:
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: dict, ttl: int = 3600) -> None:
        self.client.setex(key, ttl, json.dumps(value))

# cache/memory_cache.py -- alternative implementation
class MemoryCache(CacheInterface):
    def __init__(self):
        self._store = {}

    def get(self, key: str) -> dict | None:
        return self._store.get(key)

    def set(self, key: str, value: dict, ttl: int = 3600) -> None:
        self._store[key] = value
```

Now switching from Redis to an in-memory cache (or Memcached, or a database-backed cache) requires changing only the dependency injection configuration, not any module that uses the cache.

#### Tactic 7: Use an Intermediary

**Definition:** Introduce an indirection layer (broker, facade, mediator, proxy, adapter) between two modules so that they do not depend on each other directly.

**How it works:** When module A depends on module B, and this dependency creates problematic coupling (e.g., A would need to change whenever B changes), introduce module C between them. A depends on C, and C depends on B. Changes to B now only affect C, not A.

**ISO 25010 target:** Modularity, Modifiability

This is the tactic with the most service-oriented pattern implementations -- Bogner found 9 SOA patterns realizing this tactic, including Service Facade, Proxy Capability, and Service Broker [@bogner2019modifiability].

**Example:**

Before -- direct dependency on external payment API:

```python
# order_processor.py
import stripe

class OrderProcessor:
    def charge_customer(self, amount, customer_id):
        return stripe.Charge.create(
            amount=int(amount * 100),
            currency="usd",
            customer=customer_id
        )
```

After -- intermediary facade decouples from specific provider:

```python
# payment/gateway.py (intermediary)
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str,
               customer_ref: str) -> PaymentResult: ...

class StripeGateway(PaymentGateway):
    def charge(self, amount, currency, customer_ref):
        import stripe
        result = stripe.Charge.create(
            amount=int(amount * 100),
            currency=currency,
            customer=customer_ref
        )
        return PaymentResult(success=True, transaction_id=result.id)

class PayPalGateway(PaymentGateway):
    def charge(self, amount, currency, customer_ref):
        # PayPal-specific implementation
        ...

# order_processor.py -- depends on abstraction, not Stripe
class OrderProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def charge_customer(self, amount, customer_id):
        return self.gateway.charge(amount, "usd", customer_id)
```

#### Tactic 8: Restrict Dependencies

(See Category 1, Tactic 5 above -- this tactic appears in both the "Increase Cohesion" and "Reduce Coupling" categories in the literature because it serves both purposes: it increases cohesion by forcing modules to work within their layer, and it reduces coupling by eliminating unauthorized cross-layer dependencies.)

#### Tactic 9: Abstract Common Services

(See Category 1, Tactic 2 above -- similarly, this tactic serves both cohesion and coupling goals. By extracting common functionality, it both increases the cohesion of individual modules, which no longer contain duplicated non-core logic, and reduces coupling by creating a stable shared dependency rather than ad-hoc inter-module coupling.)

### Category 3: Defer Binding Time (6 Tactics)

Binding-time tactics postpone when design decisions take effect. The later a decision is bound, the more flexibility the system has to accommodate change without requiring code modification.

#### Tactic 10: Component Replacement

**Definition:** Design the system so that entire components can be replaced at deployment or runtime without modifying the rest of the system.

**How it works:** Define clear interfaces for components and use dependency injection, plugin architectures, or service registries to bind concrete implementations at runtime or deployment time.

**ISO 25010 target:** Modifiability, Reusability

#### Tactic 11: Publish-Subscribe

**Definition:** Decouple event producers from event consumers through an intermediary event bus or notification mechanism, so that producers do not need to know which consumers exist.

**How it works:** Instead of module A directly calling methods on modules B, C, and D when an event occurs, module A publishes an event to a bus. Modules B, C, and D subscribe to events they care about. Adding a new consumer (module E) requires no changes to the producer.

**ISO 25010 target:** Modularity, Modifiability

**Example:**

Before -- tight coupling between order creation and side effects:

```python
class OrderService:
    def __init__(self, inventory, email, analytics, loyalty):
        self.inventory = inventory
        self.email = email
        self.analytics = analytics
        self.loyalty = loyalty

    def create_order(self, order_data):
        order = self._save_order(order_data)
        self.inventory.reserve_items(order.items)     # direct call
        self.email.send_confirmation(order.customer)   # direct call
        self.analytics.track_purchase(order)           # direct call
        self.loyalty.award_points(order.customer, order.total)  # direct call
        return order
```

After -- event-driven with publish-subscribe:

```python
# events/bus.py
class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, handler):
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, data):
        for handler in self._subscribers.get(event_type, []):
            handler(data)

# order_service.py -- publishes events, does not know about subscribers
class OrderService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def create_order(self, order_data):
        order = self._save_order(order_data)
        self.event_bus.publish("order.created", order)
        return order

# Each subscriber registers independently
event_bus = EventBus()
event_bus.subscribe("order.created", inventory_service.reserve_items)
event_bus.subscribe("order.created", email_service.send_confirmation)
event_bus.subscribe("order.created", analytics_service.track_purchase)
event_bus.subscribe("order.created", loyalty_service.award_points)
```

Adding a new side effect (e.g., fraud detection) requires only adding a new subscriber -- zero changes to `OrderService`.

#### Tactic 12: Configuration Files

**Definition:** Extract hardcoded values and behavioral choices into external configuration files that are read at startup time.

**How it works:** Identify values embedded directly in source code (database URLs, feature flags, API keys, thresholds, algorithm selections) and move them to configuration files (YAML, JSON, environment variables, .ini files). The application reads these at startup and uses them to configure its behavior.

**ISO 25010 target:** Modifiability, Analysability

**Example:**

Before -- hardcoded values scattered through code:

```python
class DatabaseService:
    def connect(self):
        return psycopg2.connect(
            host="db.production.example.com",
            port=5432,
            database="myapp_prod",
            user="admin",
            password="s3cret_p@ss"
        )

class RateLimiter:
    MAX_REQUESTS = 100
    WINDOW_SECONDS = 60
```

After -- externalized to configuration:

```yaml
# config.yaml
database:
  host: ${DB_HOST}
  port: ${DB_PORT:-5432}
  name: ${DB_NAME}
  user: ${DB_USER}
  password: ${DB_PASSWORD}

rate_limiter:
  max_requests: 100
  window_seconds: 60
```

```python
# config.py
import yaml
import os

def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        config = yaml.safe_load(f)
    # Resolve environment variables
    return _resolve_env_vars(config)

# database_service.py
class DatabaseService:
    def __init__(self, config: dict):
        self.db_config = config["database"]

    def connect(self):
        return psycopg2.connect(**self.db_config)
```

#### Tactic 13: Resource Files

**Definition:** Externalize locale-specific, domain-specific, or frequently-changed content into resource files that can be modified without changing code.

**ISO 25010 target:** Modifiability

#### Tactic 14: Polymorphism

**Definition:** Use polymorphic dispatch (inheritance, protocols, or duck typing) so that the specific behavior invoked is determined by the type of the object at runtime, not by conditional logic in the caller.

**ISO 25010 target:** Modifiability

**Example:**

Before -- conditional logic selects behavior:

```python
def calculate_shipping(order, method):
    if method == "standard":
        return order.weight * 0.5
    elif method == "express":
        return order.weight * 1.5 + 10
    elif method == "overnight":
        return order.weight * 3.0 + 25
    else:
        raise ValueError(f"Unknown method: {method}")
```

After -- polymorphism delegates to the right implementation:

```python
from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, order) -> float: ...

class StandardShipping(ShippingStrategy):
    def calculate(self, order):
        return order.weight * 0.5

class ExpressShipping(ShippingStrategy):
    def calculate(self, order):
        return order.weight * 1.5 + 10

class OvernightShipping(ShippingStrategy):
    def calculate(self, order):
        return order.weight * 3.0 + 25

# Adding a new shipping method requires only a new class, no changes to callers
def calculate_shipping(order, strategy: ShippingStrategy):
    return strategy.calculate(order)
```

#### Tactic 15: Start-up Time Binding

**Definition:** Bind configuration and behavioral choices at application startup time rather than at compile time, allowing changes through configuration rather than code modification.

**ISO 25010 target:** Modifiability, Analysability

This tactic overlaps with "Configuration Files" but is broader -- it includes any mechanism that defers binding to startup: reading environment variables, loading plugin modules dynamically, selecting database drivers based on configuration, etc.

### Comprehensive Summary Table

The following table summarizes all 15 modifiability tactics with their measurability and LLM implementability assessment:

| # | Tactic | Category | ISO 25010 Target | Measurable By | LLM Implementable? |
|---|--------|----------|-----------------|---------------|-------------------|
| 1 | Split Module | Increase Cohesion | Modularity, Modifiability | Per-module CC reduction, LOC per module, module count | **Yes** -- Extract Class/Method is a well-understood refactoring |
| 2 | Abstract Common Services | Increase Cohesion | Modularity, Reusability | Duplication %, total LOC reduction, shared module count | **Yes** -- duplication detection and extraction is within LLM capability |
| 3 | Increase Semantic Coherence | Increase Cohesion | Modularity, Analysability | LCOM (Lack of Cohesion), responsibility distribution | **Yes** -- LLMs can analyze and reassign responsibilities |
| 4 | Encapsulate | Increase Cohesion | Modularity, Modifiability | Public API surface, hidden code % | **Yes** -- introducing classes/interfaces from raw data |
| 5 | Restrict Dependencies | Increase Cohesion / Reduce Coupling | Modularity, Testability | Circular dependency count, import graph depth | **Yes** -- LLMs can reorganize imports and introduce interfaces |
| 6 | Use Encapsulation | Reduce Coupling | Modularity, Modifiability | CBO, afferent/efferent coupling | **Yes** -- introducing abstract interfaces for concrete deps |
| 7 | Use an Intermediary | Reduce Coupling | Modularity, Modifiability | CBO, fan-in/fan-out, intermediary count | **Yes** -- facade/adapter introduction is a standard refactoring |
| 8 | Maintain Existing Interface | Reduce Coupling | Modifiability, Analysability | API breaking change count | **Partial** -- relevant mainly during API evolution, not snapshot refactoring |
| 9 | Anticipate Expected Changes | Increase Cohesion | Modifiability | Change propagation analysis | **No** -- requires domain knowledge about future changes |
| 10 | Generalize Module | Increase Cohesion | Reusability, Modifiability | Parameter genericity, reuse frequency | **Partial** -- risk of over-engineering without usage context |
| 11 | Publish-Subscribe | Defer Binding | Modularity, Modifiability | Direct dependency count, event channel count | **Yes** -- event bus refactoring is well-defined |
| 12 | Configuration Files | Defer Binding | Modifiability, Analysability | Hardcoded value count, config externalization ratio | **Yes** -- extracting hardcoded values is straightforward |
| 13 | Resource Files | Defer Binding | Modifiability | Resource externalization ratio | **Yes** -- simple extraction task |
| 14 | Polymorphism | Defer Binding | Modifiability | Conditional complexity reduction, strategy pattern count | **Yes** -- Replace Conditional with Polymorphism is a classic refactoring |
| 15 | Start-up Time Binding | Defer Binding | Modifiability, Analysability | Hardcoded config count, env-var usage | **Yes** -- similar to configuration file extraction |

The "LLM Implementable?" column is critical for the thesis. Of the 15 tactics, **11 are assessed as fully implementable** by an LLM through source code transformation, 2 are partially implementable, and 2 are not implementable without external domain knowledge. The thesis selects 8 tactics for its pipeline based on three criteria: (1) full LLM implementability, (2) measurability through static analysis, and (3) demonstrated structural compatibility with common backend patterns.

## 4.3 Pattern-Tactic Interactions

Tactics do not exist in isolation. In real systems, they are implemented within the context of existing architectural patterns. Understanding how tactics interact with patterns is essential for predicting whether a tactic implementation will succeed or fail.

### Harrison & Avgeriou's Interaction Model

Harrison and Avgeriou developed the definitive model for pattern-tactic interactions, based on analysis of reliability tactics across multiple patterns and validated through three industrial case studies [@harrison2010how].

#### Five Structural Interaction Types

When a tactic is implemented within a pattern, it causes structural changes to the pattern's components and connectors. Harrison identifies five types, ordered by increasing impact:

| Type | Description | Component Change | Connector Change | Impact Level | Example |
|------|-------------|-----------------|-----------------|-------------|---------|
| **Implemented-in** | Tactic behavior is added inside an existing component; no structural change to the pattern | Modified internals | None | Lowest | Adding input validation logic inside an existing Controller in MVC |
| **Replicates** | An existing component is duplicated to realize the tactic | Duplicated component | New connectors to replica | Low-Medium | Creating a read-only database replica for load distribution |
| **Add-in-pattern** | A new component is added within the existing pattern structure | New component within pattern | New connectors within pattern | Medium | Adding a Service Facade between existing layers in a Layered architecture |
| **Add-out-of-pattern** | A new component is added outside the pattern structure, crossing pattern boundaries | New component outside pattern | Connectors cross pattern boundary | High | Adding a monitoring service that bypasses the normal layered structure |
| **Modify** | An existing component is fundamentally altered in structure | Fundamentally changed | May be altered | Highest | Splitting a monolithic data store into separate per-service databases |

#### Impact Magnitude Scale

Harrison also provides a five-point qualitative scale for assessing how well a tactic fits within a given pattern:

| Rating | Meaning | Criteria |
|--------|---------|----------|
| **Good Fit (++)** | Tactic integrates naturally into the pattern | 1-2 component changes, no new connectors outside pattern |
| **Minor Changes (+)** | Tactic requires small modifications to the pattern | 3 component changes, minor connector additions |
| **Neutral (~)** | Neither naturally fitting nor conflicting | Mixed impact; some beneficial, some neutral |
| **Significant Changes (-)** | Tactic requires substantial pattern modifications | Multiple component changes and new connectors |
| **Poor Fit (--)** | Tactic conflicts with the pattern's structure | Requires adding components outside pattern, causing drift |

The practical threshold is important: **3 or fewer participant (component) changes indicate lower impact; more than 3 indicate higher impact** [@harrison2010how].

#### Behavioral Interaction Types

Beyond structural changes, tactics also affect the behavioral sequences within patterns:

1. **Adding action sequences** -- New sequences of actions are introduced within or outside existing behavioral flows
2. **Timing modifications** -- Four sub-types:
   - Adding new explicit timing constraints
   - Adding new implicit timing constraints
   - Changing existing explicit timing
   - Changing existing implicit timing

#### Architecture Drift as Snowball Effect

Harrison's most important practical finding is that tactic implementation can trigger cascading structural changes -- what he calls a "snowball effect." In one case study, adding a layer bypass for performance improvement required:

1. A new component outside the normal layer structure (Add-out-of-pattern)
2. A duplicate authorization component because the bypassed layer contained authorization logic
3. Duplicated code between the original and duplicate authorization components

The result: a tactic intended to improve performance *degraded* maintainability through code duplication and structural irregularity. Harrison's warning is direct:

> "Implementing tactics is actually a form of architecture drift." [@harrison2010how]

This finding has critical implications for LLM-based tactic implementation. The pipeline must be designed to prefer tactic implementations that are "Implemented-in" or "Add-in-pattern" types (lower impact) and to flag or avoid implementations that would create "Add-out-of-pattern" changes (high drift risk).

### Pattern-Tactic Compatibility Examples

The following table illustrates how the same tactic can have very different compatibility ratings depending on the target pattern:

| Tactic | MVC | Layered | Pipe-and-Filter | Repository | Broker |
|--------|-----|---------|-----------------|------------|--------|
| Split Module | Good Fit (++) -- natural decomposition within each layer | Good Fit (++) -- splits within a layer | Good Fit (++) -- each filter is naturally isolated | Neutral (~) | Minor (+) |
| Use an Intermediary | Minor (+) -- add a service layer between controller and model | Good Fit (++) -- intermediary layers are native to the pattern | Poor Fit (--) -- intermediaries break the pipeline flow | Good Fit (++) -- repository itself is an intermediary | Good Fit (++) -- broker is an intermediary |
| Publish-Subscribe | Minor (+) -- replace controller-model callbacks with events | Significant (-) -- events cross layer boundaries | Good Fit (++) -- filters already communicate through channels | Minor (+) | Good Fit (++) -- broker supports pub-sub natively |

### Kassab's Empirical Finding

The theoretical pattern-tactic interaction model is grounded in empirical reality by Kassab et al.'s survey of 809 software professionals [@kassab2018software]:

- **63% of real projects modify architectural patterns with tactics** during implementation
- Functionality (not quality requirements) is the primary driver for pattern selection
- Patterns are almost never applied "by the book" -- they are adapted to the project's needs

This confirms that the pattern-tactic interaction problem is not academic. Every real system that uses architectural patterns has already applied tactics (whether the developers called them that or not), and understanding these interactions is essential for any automated approach that modifies system architecture.

## 4.4 Tactics in Service-Oriented and Microservice Systems

Bogner, Wagner, and Zimmermann provide the most detailed mapping of modifiability tactics to modern service-oriented architectures [@bogner2019modifiability]. Their work systematically maps all 15 modifiability tactics onto principles and design patterns of both SOA and Microservice-Based Systems.

### Mapping Methodology

Bogner's team compiled:
- 15 modifiability tactics from Bass et al. (2003, 2012) and Bachmann et al. (2007)
- 8 SOA principles from Erl
- 8 Microservices principles from Lewis and Fowler
- 118 SOA patterns from Erl and Rotem-Gal-Oz
- 42 Microservices patterns from Richardson's catalog

They then performed a qualitative mapping, identifying which service-oriented patterns realize which modifiability tactics. The complete mapping data is publicly available on GitHub (xjreb/research-modifiability-tactics).

### Key Results

| Metric | SOA | Microservices |
|--------|-----|---------------|
| Total patterns in catalog | 118 | 42 |
| Patterns mapped to modifiability tactics | 47 (~40%) | 21 (50%) |
| Principle-to-tactic mappings | 26 of 120 possible | 15 of 120 possible |
| Principle with most tactic mappings | Service Loose Coupling (7 tactics) | Evolutionary Design (5 tactics) |
| Dominant tactic category (principles) | Reduce Coupling (16 mappings) | Reduce Coupling (7 mappings) |
| Dominant tactic category (patterns) | Reduce Coupling (23 patterns, ~49%) | Defer Binding Time (11 patterns, ~52%) |
| Tactic with most pattern matches | Use an Intermediary (9 SOA patterns) | Runtime Registration & Dynamic Lookup (5 MS patterns) |
| Tactic with zero pattern matches | Compile Time Binding (neither SOA nor MS) | Compile Time Binding (neither SOA nor MS) |

### Tactic Category Distribution

| Tactic Category | SOA Pattern % | Microservices Pattern % | Strategy |
|----------------|--------------|------------------------|----------|
| **Increase Cohesion** | 24% (11 patterns) | 14% (3 patterns) | Underrepresented in both |
| **Reduce Coupling** | 49% (23 patterns) | 33% (7 patterns) | Dominant in SOA |
| **Defer Binding Time** | 28% (13 patterns) | 52% (11 patterns) | Dominant in Microservices |

### Strategic Differences

The data reveals a fundamental strategic difference in how the two architectural styles achieve modifiability:

- **SOA** achieves modifiability through **governance, standardization, and intermediaries**. The heavy use of Reduce Coupling tactics (49% of patterns) reflects SOA's emphasis on well-defined service contracts, standardized protocols (SOAP, WSDL), and intermediary patterns (Service Facade, Service Broker, Enterprise Service Bus) that decouple services through centralized mediation.

- **Microservices** achieve modifiability through **evolutionary design, infrastructure automation, and runtime discovery**. The dominance of Defer Binding Time tactics (52% of patterns) reflects Microservices' emphasis on independent deployability, dynamic service discovery, event-driven communication, and infrastructure-as-code.

### The Cohesion Gap

A particularly striking finding is that **only 3 of 21 mapped Microservices patterns fall under "Increase Cohesion"** -- despite small, cohesive services being a core Microservices philosophy. Bogner notes that this gap may indicate that cohesion in Microservices is achieved through the decomposition philosophy itself (each service is inherently cohesive because it owns a single bounded context) rather than through specific patterns.

This cohesion gap represents an area where LLM-driven tactic implementation could add particular value: helping developers decompose services that have grown beyond their original bounded context back into cohesive units, using Split Module and Increase Semantic Coherence tactics.

## 4.5 The Tactic Research Landscape

Marquez, Astudillo, and Kazman provide the most comprehensive overview of the state of architectural tactics research through their systematic mapping study of 91 primary studies spanning 2003-2021 [@marquez2022architectural].

### Scale and Scope

| Dimension | Value |
|-----------|-------|
| Studies screened | 552 candidates from 7 digital libraries |
| Primary studies selected | 91 (79 database search + 12 snowballing) |
| Time span | 2003-2021 (18 years) |
| Digital libraries | IEEE Xplore, SpringerLink, Scopus, ACM, Web of Science, ScienceDirect, Wiley |
| Quality attributes covered | 12 (original 7 + adaptability, dependability, reliability, deployability, scalability, fault tolerance, safety) |

### The Rigor Gap

The most sobering finding is the pervasive lack of methodological rigor:

| Methodological Aspect | Studies Lacking It | Percentage |
|----------------------|-------------------|-----------|
| Tactic identification method not described | 65 of 91 | **71%** |
| Data source for recognizing tactics not described | 63 of 91 | **69%** |
| Tactic description/characterization mechanism not described | 54 of 91 | **59%** |

Marquez concludes:

> "Little rigor has been used to characterize and define architectural tactics; most architectural tactics proposed in the literature do not conform to the original definition." [@marquez2022architectural]

### Quality Attribute Coverage Imbalance

| Quality Attribute | # of Dedicated Studies | Research Maturity |
|-------------------|----------------------|-------------------|
| Security | 18 | Well-studied |
| Fault Tolerance | 5 | Moderate |
| Availability | 4 | Moderate |
| Performance | 4 | Moderate |
| Safety | 4 | Moderate |
| **Modifiability** | **1** | **Severely under-researched** |
| Testability | 0 | Not studied |

The fact that modifiability -- the quality attribute most directly related to ISO 25010 maintainability -- has received exactly one dedicated study out of 91 is a critical research gap. This thesis directly addresses this gap.

### Detection Tools and Techniques

The mapping study catalogues existing tactic detection approaches:

| Technique | # of Studies | Tools |
|-----------|-------------|-------|
| Manual mapping | 10 | Expert judgment |
| Code analysis | 10 | Custom scripts, AST analysis |
| Text analysis / NLP | 4 | BERT classifiers, LDA topic modeling |
| Multifacetic (combined) | 3 | Archie, ArchEngine, ARCODE |
| Machine learning | Subset of above | SVM, Decision Trees, Bayesian LR, AdaBoost |
| Not described | 65 | N/A |

Critically, **all existing tools detect tactics but none implement them**. The detection-to-implementation gap is the central motivation for the thesis. As Marquez notes:

> "Tactics have become relevant to map architecture decisions onto source code, and automation opportunities beckon within reach." [@marquez2022architectural]

### Research Type Distribution

| Research Type | Percentage |
|--------------|-----------|
| Solution proposals (new methods/tools) | 47.3% |
| Evaluation research (applying methods) | 39.6% |
| Philosophical / experience papers | 13.1% |

| Contribution Type | Percentage |
|-------------------|-----------|
| Frameworks | 48.4% |
| Models | 16.5% |
| Guidelines | 15.4% |
| Lessons learned | 7.7% |
| Theories | 6.6% |

The dominance of frameworks and solution proposals indicates a field still in the theory-building phase. The thesis contributes to moving the field toward implementation and empirical validation.

## 4.6 Quality-Driven Architecture Development

### Kim's Feature Model Approach

Kim, Kim, Lu, and Park proposed the most rigorous formalization of architectural tactics, using feature models to capture tactic variability and the Role-Based Metamodeling Language (RBML) to specify structural and behavioral semantics [@kim2009qualitydriven].

#### Feature Models for Tactic Relationships

Feature models capture five types of relationships between tactics:

| Relationship | Meaning | Example |
|-------------|---------|---------|
| **Mandatory** | If the parent tactic category is selected, this tactic must be included | Fault Detection is mandatory for any Availability strategy |
| **Optional** | May or may not be included | State Resynchronization is optional within Recovery |
| **Requires** | Selecting tactic A requires also selecting tactic B | Active Redundancy requires Heartbeat for failure detection |
| **Suggested** | Selecting tactic A makes tactic B advisable but not required | Checkpoint/Rollback suggests State Resynchronization for faster recovery |
| **Mutually exclusive** | Selecting tactic A prevents selecting tactic B | Active Redundancy and Passive Redundancy are mutually exclusive |

#### RBML Specifications

For each formalized tactic, Kim provides:
- **Structural specification:** UML class diagram roles showing required components, interfaces, and relationships
- **Behavioral specification:** Sequence diagram showing the expected interaction pattern
- **Realization multiplicity:** How many instances of each role are valid (e.g., 1 FIFO queue vs. 3 FIFO queues)

#### Coverage and Limitations

Kim successfully formalized tactics for three quality attributes:

| Quality Attribute | Tactics Formalized |
|-------------------|-------------------|
| Availability | Fault Detection (Ping/Echo, Heartbeat, Exception), Recovery Reintroduction (Checkpoint/Rollback, State Resynchronization), Recovery Preparation and Repair (Voting, Active Redundancy, Passive Redundancy) |
| Performance | Resource Arbitration (FIFO, Fixed Priority Scheduling, Dynamic Priority Scheduling), Resource Management (Introduce Concurrency, Maintain Multiple Copies/Cache) |
| Security | Resisting Attacks (Authentication: ID/Password, One-time Password; Authorization; Maintain Data Confidentiality), Recovering from Attacks (Restoration) |

**Modifiability is explicitly listed as future work.** Kim notes:

> "It should be noted that not all tactics can be specified in the RBML. For instance, the resource demand tactics, which are concerned with managing resource demand, are difficult to formalize in the RBML due to the abstract nature of their solutions." [@kim2009qualitydriven]

This is a key gap the thesis addresses. While formal RBML specifications for modifiability tactics do not exist, the feature model relationship types (requires, suggested, mutually exclusive) are transferable and can be encoded as structured constraints in the LLM prompt chain. For example:
- "Split Module" **requires** that the target module has multiple identifiable responsibilities
- "Use an Intermediary" **suggests** prior application of "Use Encapsulation"
- "Publish-Subscribe" and direct method invocation are **mutually exclusive** for the same interaction

### Rahmati's Pattern Evaluation Framework

Rahmati and Tanhaei provide a complementary approach at the pattern level [@rahmati2021ensuring]. Instead of formalizing individual tactics, they evaluate how well entire architectural patterns support maintainability.

#### The Maintainability Hexagon

Their quality model decomposes maintainability into six sub-attributes, each scored on a 0-4 scale:

| Score | Meaning |
|-------|---------|
| 0 | Large reduction in this sub-attribute |
| 1 | Relative reduction |
| 2 | Neutral |
| 3 | Relative increase |
| 4 | Large increase |

#### Pattern Radar Scores

| Pattern | Testability | Changeability | Understandability | Portability | Stability | Analysability |
|---------|-------------|---------------|-------------------|-------------|-----------|---------------|
| **Multi-Layered** | 4 | 4 | 2 | 4 | 3 | 3 |
| **MVC** | 4 | 4 | 3 | 4 | 2 | 3 |
| **Broker** | 4 | 4 | 2 | 3 | 2 | 4 |
| **Object-Oriented** | 3 | 3 | 3 | 3 | 3 | 3 |
| **Repository** | 3 | 3 | 3 | 2 | 4 | 3 |
| **Pipe & Filter** | 1 | 4 | 0 | 3 | 2 | 0 |
| **Blackboard** | 1 | 4 | 0 | 1 | 2 | 0 |

Multi-Layered and Broker patterns achieve the highest overall maintainability scores. Pipe & Filter excels in changeability but scores poorly in testability, understandability, and analysability -- a cautionary example that optimizing for one sub-attribute can come at the cost of others.

#### Case Study Evidence

Rahmati's two case studies provide critical empirical evidence:

**Case Study 1 (Successful):** A university research management system was refactored from a Proxy-based architecture to MVC. The result:
- **50-64% average reduction in maintenance effort** across multiple maintenance scenarios
- Improvement increased over time (12-14% additional improvement in subsequent months) as the team became more familiar with the new structure

**Case Study 2 (Failed):** A commercial PHP CMS was refactored from flat, unstructured code to MVC using the Yii Framework. The result:
- **~10% increase in maintenance effort** -- the refactoring made things worse
- The system was already simple enough that the MVC overhead added complexity without proportional benefit
- The team was unfamiliar with the target framework, adding a learning curve

The lesson is sharp:

> "Architecture patterns are preventing rather than preserving in maintainability aspects." [@rahmati2021ensuring]

This means that patterns *prevent* maintainability problems from arising in appropriate contexts, but they cannot *guarantee* maintainability if the lower-level implementation is flawed or if the pattern is misapplied. For the thesis, this finding reinforces that LLM-driven tactic implementation must:

1. **Assess the current system's complexity** before recommending architectural changes
2. **Match tactics to the target architecture** -- not all tactics improve all systems
3. **Ensure correct lower-level realization** -- the LLM must generate not just structurally correct but semantically correct code

### Connecting Kim and Rahmati

The relationship between Kim's tactic-level formalization and Rahmati's pattern-level evaluation provides a layered decision framework:

1. **Rahmati's radar model** identifies *which maintainability sub-attributes are deficient* in the current system
2. **Bass's tactic catalog** identifies *which tactics target those specific sub-attributes*
3. **Kim's feature model relationships** constrain *which tactic combinations are valid*
4. **Harrison's interaction model** predicts *how well those tactics fit within the current architecture pattern*

This layered approach is what the thesis LLM pipeline must encode in its prompt chain: detect the architecture, assess the quality deficiencies, select appropriate tactics, verify pattern compatibility, and then implement.

## Summary

This chapter established the theoretical foundation for architectural tactics and their role in improving software maintainability. The key takeaways are:

1. **Architectural tactics are fine-grained building blocks** that target single quality attribute responses, distinct from patterns (which package multiple tactics with built-in tradeoffs) and design techniques (which implement tactics at the code level) [@bass2021software].

2. **The modifiability catalog contains 15 tactics** in three categories: Increase Cohesion (5), Reduce Coupling (4), and Defer Binding Time (6). Of these, 11 are assessed as fully implementable by an LLM through source code transformation.

3. **Pattern-tactic interactions vary widely** from Good Fit to Poor Fit, and poorly chosen tactic implementations can cause architecture drift with cascading maintainability degradation [@harrison2010how]. LLM-based implementation must respect pattern boundaries.

4. **SOA and Microservices achieve modifiability through different strategies**: SOA through governance and intermediaries (Reduce Coupling dominant), Microservices through evolutionary design and runtime discovery (Defer Binding Time dominant) [@bogner2019modifiability].

5. **The research landscape has critical gaps**: modifiability has received only 1 dedicated study out of 91, 71% of studies lack methodological rigor in tactic identification, and no existing tool implements tactics automatically [@marquez2022architectural].

6. **Kim's feature model formalization** provides composability rules for tactics, but does not cover modifiability -- a gap this thesis addresses [@kim2009qualitydriven].

7. **Rahmati's case studies** demonstrate that architecture-level refactoring can improve maintainability by 50-64% when well-matched, but can degrade it by 10% when misapplied [@rahmati2021ensuring] -- underscoring the need for systematic, context-aware tactic selection.

8. **The detection-implementation gap** is the central problem: existing tools can detect tactics in code but cannot implement them. The thesis proposes that LLMs, augmented with architectural context and structured tactic specifications, can bridge this gap for maintainability tactics.
