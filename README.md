# pogodynka-tai


# Database

# Endpoints

### */forecast/<int:favorite_id>*

Methods: GET

Only for logged in users.

Get the forecast for one of the favourites. Calls OpenWeather API. 

**Parameters**

|      Name |  Type   | Description                           |
| ---------:|:-------:| ------------------------------------- |
|    `favorite_id` | int    | Id of the favourite    |

**Response**

HTML site. 7 days of forecast including: date, description, day temperature[°C], night temperature[°C], humidity[%] and wind speed[km/h].

### */add_favourite*

Methods: GET, POST

Only for logged in users.

Add a place defined by coordinates to favourites.

**Parameters**

|      Name |  Type   | Description                           |
| ---------:|:-------:| ------------------------------------- |
|    `name` | text    | Name of the favourite to be added.    |
|     `lat` | number  | Coordinates: latitude<br/><br/>Step 0.0001         |
|     `lon` | number  | Coordinates: Longitude<br/><br/>Step 0.0001        |

### */delete/<int:user_id>*

Methods: GET

Only for logged in users. Only for administrator.

Delete user.

**Parameters**

|      Name |  Type   | Description                           |
| ---------:|:-------:| ------------------------------------- |
|    `user_id` | int    | Id of the user to delete.    |

### */weather*

Methods: GET

Only for logged in users.

Current weather for all favourites. Calls OpenWeather API.

**Parameters**

None

**Response**

HTML site. Current weather for all favourites: name, description, temperature[°C], humidity[%].

### */deleteFavorite/<int:favorite_id>*

Methods: GET

Only for logged in users.

Delete favourite.

**Parameters**

|      Name |  Type   | Description                           |
| ---------:|:-------:| ------------------------------------- |
|    `favorite_id` | int    | Id of the favourite to delete.    |

### */users*

Methods: GET

Only for logged in users. Only for administrator.

Get users.

**Parameters**

None.

**Response**

HTML site. List of registered users.

### */register*

Methods: GET, POST

Requires completing ReCaptcha.

Crete a new user.

**Parameters**

|      Name |  Type   | Description                           |
| ---------:|:-------:| ------------------------------------- |
|    `name` | text    | Username. At least 5 characters. Max 255 characters. Unique.   |
|     `password` | password  | Password. Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.         |
|     `confirm` | password  | Repeat password. Has to match with  `password`. Max 255 characters.     |

### */login*

Methods: GET, POST

Sign in to existing account.

**Parameters**

|      Name |  Type   | Description                           |
| ---------:|:-------:| ------------------------------------- |
|    `name` | text    | Username  |
|     `password` | password  | Password        |

### */logout*

Methods: GET

Sign out.

**Parameters**

None

