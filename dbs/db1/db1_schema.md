# Database Schema Description

## Tables and Relationships

### Systems
- **Description**: Contains information about all IT systems in the organization.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the system
  - `name` (TEXT, NOT NULL): System name
  - `description` (TEXT): Details about the system's purpose and functionality
  - `kind` (TEXT): Type of system, can be one of: 'app', 'db', 'server', 'network', 'external', 'storage', 'virtualization', 'integration'; defaults to 'app'

### Dependencies
- **Description**: Represents relationships between systems, indicating which systems depend on others.
- **Fields**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the dependency relationship
  - `from_system_id` (TEXT, FOREIGN KEY → Systems.id): The dependent system
  - `to_system_id` (TEXT, FOREIGN KEY → Systems.id): The system being depended upon
  - `description` (TEXT): Details about the nature of the dependency

### Domains
- **Description**: Represents business domains within the organization.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the domain
  - `description` (TEXT): Description of the business domain

### BoundedContexts
- **Description**: Represents bounded contexts within domains (from Domain-Driven Design).
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the bounded context
  - `domain_id` (TEXT, FOREIGN KEY → Domains.id): The domain this bounded context belongs to
  - `description` (TEXT): Description of the bounded context

### Systems_BoundedContexts
- **Description**: Junction table mapping systems to bounded contexts (many-to-many relationship).
- **Fields**:
  - `system_id` (TEXT, FOREIGN KEY → Systems.id): Reference to a system
  - `bounded_context_id` (TEXT, FOREIGN KEY → BoundedContexts.id): Reference to a bounded context
  - Combined PRIMARY KEY of (system_id, bounded_context_id)

### Departments
- **Description**: Represents organizational departments within the company.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the department
  - `manager_id` (INTEGER, FOREIGN KEY → Employees.id): ID of the employee who manages the department

### Employees
- **Description**: Contains information about company employees.
- **Fields**:
  - `id` (INTEGER, PRIMARY KEY): Unique identifier for the employee
  - `name` (TEXT, NOT NULL): Employee's full name
  - `role` (TEXT): Employee's job title or role
  - `department_id` (TEXT, FOREIGN KEY → Departments.id): Department the employee belongs to
  - `manager_id` (INTEGER, FOREIGN KEY → Employees.id): ID of the employee's manager

### SystemResponsibilities
- **Description**: Maps employees to systems with specific responsibility types.
- **Fields**:
  - `system_id` (TEXT, FOREIGN KEY → Systems.id): The system
  - `employee_id` (INTEGER, FOREIGN KEY → Employees.id): The responsible employee
  - `responsibility_type` (TEXT): Type of responsibility, either 'owner' or 'maintainer'
  - Combined PRIMARY KEY of (system_id, employee_id, responsibility_type)

### Company
- **Description**: Represents the company entity itself.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the company

## Key Relationships

1. Systems can have multiple dependencies on other systems
2. Systems can belong to multiple bounded contexts
3. Bounded contexts belong to specific business domains
4. Employees can be responsible for multiple systems (as owners or maintainers)
5. Systems can have multiple employees responsible for them
6. Employees belong to departments and report to managers
7. Departments have managers who are employees

## Common Query Patterns

- Finding all systems a specific employee is responsible for
- Finding all employees responsible for a specific system
- Identifying systems with dependencies on a given system
- Listing systems by their type/kind
- Finding systems within specific bounded contexts or domains
- Organizational hierarchy queries through the employee-manager relationship