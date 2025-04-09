# Database Schema Description


## Tables and Relationships

### System
- **Description**: Contains information about all IT systems in the organization.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the system
  - `name` (TEXT, NOT NULL): System name
  - `description` (TEXT): Details about the system's purpose and functionality
  - `kind` (TEXT): Type of system, can be: 'app', 'db', 'server', 'network', 'external', 'storage', 'virtualization', 'integration'; defaults to 'app'
  - `location` (TEXT): Physical or logical location of the system
  - `installation_date` (TEXT): When the system was installed/deployed
  - `decommission_date` (TEXT): When the system was or will be decommissioned
  - `technology_stack` (TEXT): Overview of the technology stack used

### System_ProgrammingLanguages
- **Description**: Links systems to their programming languages (many-to-many relationship).
- **Fields**:
  - `system_id` (TEXT, FOREIGN KEY → System.id): Reference to a system
  - `programming_language` (TEXT): Programming language used in the system

### System_Frameworks
- **Description**: Links systems to their frameworks (many-to-many relationship).
- **Fields**:
  - `system_id` (TEXT, FOREIGN KEY → System.id): Reference to a system
  - `framework` (TEXT): Framework used in the system

### Dependency
- **Description**: Represents relationships between systems, indicating which systems depend on others.
- **Fields**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the dependency relationship
  - `from_system_id` (TEXT, FOREIGN KEY → System.id): The dependent system
  - `to_system_id` (TEXT, FOREIGN KEY → System.id): The system being depended upon
  - `description` (TEXT): Details about the nature of the dependency

### Domain
- **Description**: Represents business domains within the organization.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the domain
  - `description` (TEXT): Description of the business domain

### BoundedContext
- **Description**: Represents bounded contexts within domains (from Domain-Driven Design).
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the bounded context
  - `description` (TEXT): Description of the bounded context
  - `domain_id` (TEXT, FOREIGN KEY → Domain.id): The domain this bounded context belongs to

### BoundedContext_System
- **Description**: Junction table mapping systems to bounded contexts (many-to-many relationship).
- **Fields**:
  - `bounded_context_id` (TEXT, FOREIGN KEY → BoundedContext.id): Reference to a bounded context
  - `system_id` (TEXT, FOREIGN KEY → System.id): Reference to a system

### Department
- **Description**: Represents organizational departments within the company.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the department
  - `manager_id` (INTEGER, FOREIGN KEY → Employee.id): ID of the employee who manages the department

### Employee
- **Description**: Contains detailed information about company employees.
- **Fields**:
  - `id` (INTEGER, PRIMARY KEY): Unique identifier for the employee
  - `name` (TEXT, NOT NULL): Employee's full name
  - `role` (TEXT): Employee's job title or role
  - `level` (TEXT): Seniority or organizational level
  - `specialization` (TEXT): Employee's area of specialization or expertise
  - `department_id` (TEXT, FOREIGN KEY → Department.id): Department the employee belongs to
  - `manager_id` (INTEGER, FOREIGN KEY → Employee.id): ID of the employee's manager
  - `location` (TEXT): Employee's physical or remote work location
  - `hire_date` (TEXT): Date when the employee was hired
  - `tenure` (INTEGER): Length of employment in the organization

### Department_Employee
- **Description**: Junction table mapping employees to departments (many-to-many relationship).
- **Fields**:
  - `department_id` (TEXT, FOREIGN KEY → Department.id): Reference to a department
  - `employee_id` (INTEGER, FOREIGN KEY → Employee.id): Reference to an employee

### TechnicalInfrastructure_System
- **Description**: Links technical infrastructure components to systems.
- **Fields**:
  - `technical_infrastructure_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the infrastructure component
  - `system_id` (TEXT, FOREIGN KEY → System.id): The system associated with this infrastructure

### SystemResponsibility
- **Description**: Maps employees to systems with specific responsibility types.
- **Fields**:
  - `system_code` (TEXT, FOREIGN KEY → System.id): The system
  - `responsibility_type` (TEXT): Type of responsibility, either 'owner' or 'maintainer'
  - `employee_id` (INTEGER, FOREIGN KEY → Employee.id): The responsible employee
  - Combined PRIMARY KEY of (system_code, responsibility_type, employee_id)

### Company
- **Description**: Represents the company entity itself.
- **Fields**:
  - `id` (TEXT, PRIMARY KEY): Unique identifier for the company

### Company_Domain
- **Description**: Links companies to domains (many-to-many relationship).
- **Fields**:
  - `company_id` (TEXT, FOREIGN KEY → Company.id): Reference to a company
  - `domain_id` (TEXT, FOREIGN KEY → Domain.id): Reference to a domain

### Company_Department
- **Description**: Links companies to departments (many-to-many relationship).
- **Fields**:
  - `company_id` (TEXT, FOREIGN KEY → Company.id): Reference to a company
  - `department_id` (TEXT, FOREIGN KEY → Department.id): Reference to a department

### Company_Employee
- **Description**: Links companies to employees (many-to-many relationship).
- **Fields**:
  - `company_id` (TEXT, FOREIGN KEY → Company.id): Reference to a company
  - `employee_id` (INTEGER, FOREIGN KEY → Employee.id): Reference to an employee
