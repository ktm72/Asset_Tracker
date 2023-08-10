# ERD of the project

![Different Relational Table](./content/assets_tracker_erd.png)

# Install Pipenv

`pip install pipenv`

## Install Dependencies

`pipenv install`

## Activate virtualenv

`pipenv shell`

## Deactivate project

`ctrl+D or exit`

# API

- localhost:8000/
  - api/test -> test purpose
  - api/company ->GET(show all), POST(entry a company)
  - api/company/1 ->GET(company details), PATCH(update company), DELETE(delete a company)
  - api/employee -> GET(show all employee), POST(entry an Employee)
  - api/employee -> GET(Employee details with company details), PATCH(update an Employee), DELETE(delete an employee)
  - api/company/1/employees -> GET(all employees under a company)
  - api/company/1/employees?status=boolean -> GET(current or former employees under a company)
  - api/gear ->GET(show all), POST(entry a gear)
  - api/gear/1 ->GET(gear details), PATCH(update gear), DELETE(delete a gear)
  - api/company/1/gears -> GET(all gears under a company)
