# TeamUp

This is the backend API of the TeamUp app. A web application for finding early tech and design professionals to find others to collaborate with.

## API Reference

#### Check if a user already exists with a certain email

```http
  GET /api/checkuser/${email}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**: an email to check for. |

#### Create a new user

```http
  POST /api/signup
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `first_name`      | `string` | **Required**. |
| `last_name`      | `string` | **Required**. |
| `email`      | `string` | **Required**. |
| `password`      | `string` | **Required**. |

