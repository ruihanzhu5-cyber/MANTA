# Trajectory: 6171bbc_1

- Benchmark: appworld
- System: MANTA_NATIVE
- Topology: self_evolved
- Run Index: 0

## Final

- Final Reason: self_evolved:no_meaningful_change
- Vote Tally: `{"i ll start by getting the supervisor s credentials and profile to log in": 2}`

### Final Answer

I'll start by getting the supervisor's credentials and profile to log in.

## Tool Definitions

### api_docs__show_app_descriptions
Show descriptions for all apps available.

```json
{
  "properties": {},
  "type": "object"
}
```

### api_docs__show_api_descriptions
Show descriptions for all APIs available for a given app.

```json
{
  "properties": {
    "app_name": {
      "description": "App name to return API descriptions for.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### api_docs__show_api_doc
Show detailed API doc.

```json
{
  "properties": {
    "api_name": {
      "description": "Name of the API.",
      "type": "string"
    },
    "app_name": {
      "description": "App name for the API.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### api_docs__search_api_docs
Search for relevant API docs.

```json
{
  "properties": {
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### supervisor__show_active_task
Show the currently active task assigned to you by the supervisor.

```json
{
  "properties": {},
  "type": "object"
}
```

### supervisor__complete_task
Mark the currently active task as complete with the given answer.

```json
{
  "properties": {
    "answer": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "integer"
        },
        {
          "type": "string"
        }
      ],
      "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
    },
    "status": {
      "default": "success",
      "description": "Mark the task complete.",
      "enum": [
        "success",
        "fail"
      ],
      "type": "string"
    }
  },
  "type": "object"
}
```

### supervisor__show_profile
Show your supervisor's profile information.

```json
{
  "properties": {},
  "type": "object"
}
```

### supervisor__show_addresses
Show your supervisor's addresses.

```json
{
  "properties": {},
  "type": "object"
}
```

### supervisor__show_payment_cards
Show your supervisor's payment_cards.

```json
{
  "properties": {},
  "type": "object"
}
```

### supervisor__show_account_passwords
Show your supervisor's app account passwords.

```json
{
  "properties": {},
  "type": "object"
}
```

### spotify__show_account
Show your account information. Unlike show_profile, this includes private information.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__signup
Sign up to create account.

```json
{
  "properties": {
    "email": {
      "description": "Your email address.",
      "format": "email",
      "type": "string"
    },
    "first_name": {
      "description": "Your first name",
      "minLength": 1,
      "type": "string"
    },
    "last_name": {
      "description": "Your last name",
      "minLength": 1,
      "type": "string"
    },
    "password": {
      "description": "Your password.",
      "minLength": 5,
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__delete_account
Delete your account.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__update_account_name
Update your first or last name in the account profile.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "first_name": {
      "description": "Your updated first name.",
      "minLength": 1,
      "type": "string"
    },
    "last_name": {
      "description": "Your updated last name.",
      "minLength": 1,
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__login
Login to your account.

```json
{
  "properties": {
    "password": {
      "description": "Your account password.",
      "type": "string"
    },
    "username": {
      "description": "Your account email.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__logout
Logout from your account.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__send_verification_code
Send account verification code to your email address.

```json
{
  "properties": {
    "email": {
      "description": "Your email address.",
      "format": "email",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__verify_account
Verify your account using the verification code sent to your email address.

```json
{
  "properties": {
    "email": {
      "description": "Your email address.",
      "format": "email",
      "type": "string"
    },
    "verification_code": {
      "description": "The verification code sent to your email address.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__send_password_reset_code
Send password reset code to your email address.

```json
{
  "properties": {
    "email": {
      "description": "Your email address.",
      "format": "email",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__reset_password
Reset your password using the password reset code sent to your email address.

```json
{
  "properties": {
    "email": {
      "description": "Your email address.",
      "format": "email",
      "type": "string"
    },
    "new_password": {
      "description": "Your new password.",
      "minLength": 5,
      "type": "string"
    },
    "password_reset_code": {
      "description": "The password reset code sent to your email address.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_profile
Show public profile information of a user.

```json
{
  "properties": {
    "email": {
      "description": "Email of the person you want to see the profile information of.",
      "format": "email",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_genres
Show the list of all music genres.

```json
{
  "properties": {},
  "type": "object"
}
```

### spotify__search_songs
Search for songs with a query.

```json
{
  "properties": {
    "album_id": {
      "description": "The album id to filter the search results by.",
      "type": "integer"
    },
    "artist_id": {
      "description": "The artist id to filter the search results by.",
      "type": "integer"
    },
    "genre": {
      "description": "The genre to filter the albums by.",
      "type": "string"
    },
    "max_duration": {
      "default": 9223372036854775807,
      "description": "The maximum duration in seconds for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "max_like_count": {
      "default": 9223372036854775807,
      "description": "The maximum like count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "max_play_count": {
      "default": 9223372036854775807,
      "description": "The maximum play count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "max_rating": {
      "default": 5,
      "description": "The maximum rating for search results.",
      "maximum": 5.0,
      "minimum": 0.0,
      "type": "number"
    },
    "max_release_date": {
      "default": "3000-01-01",
      "description": "The maximum release date for search results in YYYY-MM-DD format.",
      "type": "string"
    },
    "min_duration": {
      "default": 0,
      "description": "The minimum duration in seconds for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "min_like_count": {
      "default": 0,
      "description": "The minimum like count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "min_play_count": {
      "default": 0,
      "description": "The minimum play count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "min_rating": {
      "default": 0,
      "description": "The minimum rating for search results.",
      "maximum": 5.0,
      "minimum": 0.0,
      "type": "number"
    },
    "min_release_date": {
      "default": "1500-01-01",
      "description": "The minimum release date for search results in YYYY-MM-DD format.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "sort_by": {
      "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_song
Get details of a specific song.

```json
{
  "properties": {
    "song_id": {
      "description": "The song id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_song_privates
Show information about the song that is private to the user.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__like_song
Like a song.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to like.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__unlike_song
Unlike a song.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to unlike.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_liked_songs
Get a list of songs you have liked.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "sort_by": {
      "default": "-liked_at",
      "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__search_albums
Search for albums with a query.

```json
{
  "properties": {
    "genre": {
      "description": "The genre to filter the albums by.",
      "type": "string"
    },
    "max_like_count": {
      "default": 9223372036854775807,
      "description": "The maximum like count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "max_rating": {
      "default": 5,
      "description": "The maximum rating for search results.",
      "maximum": 5.0,
      "minimum": 0.0,
      "type": "number"
    },
    "max_release_date": {
      "default": "3000-01-01",
      "description": "The maximum release date for search results in YYYY-MM-DD format.",
      "type": "string"
    },
    "min_like_count": {
      "default": 0,
      "description": "The minimum like count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "min_rating": {
      "default": 0,
      "description": "The minimum rating for search results.",
      "maximum": 5.0,
      "minimum": 0.0,
      "type": "number"
    },
    "min_release_date": {
      "default": "1500-01-01",
      "description": "The minimum release date for search results in YYYY-MM-DD format.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "sort_by": {
      "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_album
Get details of a specific album.

```json
{
  "properties": {
    "album_id": {
      "description": "The album id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_album_privates
Show information about the album that is private to the user.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "The album id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__like_album
Like a album.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "The album id to like.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__unlike_album
Unlike a album.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "The album id to unlike.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_liked_albums
Get a list of albums you have liked.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "sort_by": {
      "default": "-liked_at",
      "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_playlist_library
Get a list of playlists in the user's playlist library.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "is_public": {
      "description": "Whether to show public playlists or private playlists.",
      "type": "boolean"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__search_playlists
Search for playlists with a query. It will search over all public playlists and your own private playlists.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "max_like_count": {
      "default": 9223372036854775807,
      "description": "The maximum like count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "max_rating": {
      "default": 5,
      "description": "The maximum rating for search results.",
      "maximum": 5.0,
      "minimum": 0.0,
      "type": "number"
    },
    "min_like_count": {
      "default": 0,
      "description": "The minimum like count for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "min_rating": {
      "default": 0,
      "description": "The minimum rating for search results.",
      "maximum": 5.0,
      "minimum": 0.0,
      "type": "number"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "sort_by": {
      "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__create_playlist
Create a new playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "is_public": {
      "default": false,
      "description": "Whether the playlist is public or not.",
      "type": "boolean"
    },
    "title": {
      "description": "The title of the playlist.",
      "minLength": 1,
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_playlist
Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "The playlist id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__delete_playlist
Delete a playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "The playlist id to delete.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__update_playlist
Update a playlist title or privacy.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "is_public": {
      "description": "Whether the playlist is public or not.",
      "type": "boolean"
    },
    "playlist_id": {
      "description": "The playlist id to update.",
      "type": "integer"
    },
    "title": {
      "description": "The updated title of the playlist.",
      "minLength": 1,
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_playlist_privates
Show information about the playlist that is private to the user.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "The playlist id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__like_playlist
Like a playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "The playlist id to like.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__unlike_playlist
Unlike a playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "The playlist id to unlike.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_liked_playlists
Get a list of playlists you have liked.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "sort_by": {
      "default": "-liked_at",
      "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__search_artists
Search for artists with a query.

```json
{
  "properties": {
    "genre": {
      "description": "The genre to filter the artists by.",
      "type": "string"
    },
    "max_follower_count": {
      "default": 9223372036854775807,
      "description": "The maximum number of followers for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "min_follower_count": {
      "default": 0,
      "description": "The minimum number of followers for search results.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "sort_by": {
      "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_artist
Get details of a specific artist.

```json
{
  "properties": {
    "artist_id": {
      "description": "The artist id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_artist_following
Show if the user is following the artist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "artist_id": {
      "description": "The artist id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_song_library
Get a list of songs in the user's song library.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__add_song_to_library
Add a song to the user's song library.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to add.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__remove_song_from_library
Remove a song from the user's song library.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to remove.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_album_library
Get a list of albums in the user's album library.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__add_album_to_library
Add an album to the user's album library.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "The album id to add.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__remove_album_from_library
Remove an album from the user's album library.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "The album id to remove.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__add_song_to_playlist
Add a song to a playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "The playlist id to add the song to.",
      "type": "integer"
    },
    "song_id": {
      "description": "The song id to add.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__remove_song_from_playlist
Remove a song from a playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "The playlist id to remove the song from.",
      "type": "integer"
    },
    "song_id": {
      "description": "The song id to remove.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_downloaded_songs
Get a list of downloaded songs.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "max_downloaded_at": {
      "default": "3000-01-01",
      "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
      "type": "string"
    },
    "min_downloaded_at": {
      "default": "1500-01-01",
      "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "sort_by": {
      "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__download_song
Download a song.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to download.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__remove_downloaded_song
Remove a song from downloads.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to remove from downloads.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_following_artists
Get a list of artists the user is following.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__follow_artist
Follow an artist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "artist_id": {
      "description": "The artist id to follow.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__unfollow_artist
Unfollow an artist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "artist_id": {
      "description": "The artist id to unfollow.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_song_reviews
Get a list of reviews for a song.

```json
{
  "properties": {
    "max_rating": {
      "default": 5,
      "description": "The maximum rating for a review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "min_rating": {
      "default": 1,
      "description": "The minimum rating for a review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "song_id": {
      "description": "The song id to retrieve reviews for.",
      "type": "integer"
    },
    "sort_by": {
      "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page.",
      "type": "string"
    },
    "user_email": {
      "description": "Email of the user to filter reviews by.",
      "format": "email",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__review_song
Rate or review a song.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "rating": {
      "description": "Song rating for this review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "song_id": {
      "description": "ID of the song to review.",
      "type": "integer"
    },
    "text": {
      "default": "",
      "description": "Text content of the review.",
      "type": "string"
    },
    "title": {
      "default": "",
      "description": "Title of the review.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_song_review
Show a song review.

```json
{
  "properties": {
    "review_id": {
      "description": "The song review id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__delete_song_review
Delete a song review.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "review_id": {
      "description": "ID of the song review.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__update_song_review
Update a song review.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "rating": {
      "description": "Song rating for this review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "review_id": {
      "description": "ID of the song review.",
      "type": "integer"
    },
    "text": {
      "description": "Text content of the review.",
      "type": "string"
    },
    "title": {
      "description": "Title of the review.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_album_reviews
Get a list of reviews for an album.

```json
{
  "properties": {
    "album_id": {
      "description": "The album id to retrieve reviews for.",
      "type": "integer"
    },
    "max_rating": {
      "default": 5,
      "description": "The maximum rating for a review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "min_rating": {
      "default": 1,
      "description": "The minimum rating for a review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "sort_by": {
      "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page.",
      "type": "string"
    },
    "user_email": {
      "description": "Email of the user to filter reviews by.",
      "format": "email",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__review_album
Rate or review an album.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "ID of the album to review.",
      "type": "integer"
    },
    "rating": {
      "description": "Album rating for this review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "text": {
      "default": "",
      "description": "Text content of the review.",
      "type": "string"
    },
    "title": {
      "default": "",
      "description": "Title of the review.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_album_review
Show an album review.

```json
{
  "properties": {
    "review_id": {
      "description": "The album review id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__delete_album_review
Delete an album review.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "review_id": {
      "description": "ID of the album review.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__update_album_review
Update an album review.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "rating": {
      "description": "Album rating for this review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "review_id": {
      "description": "ID of the album review.",
      "type": "integer"
    },
    "text": {
      "description": "Text content of the review.",
      "type": "string"
    },
    "title": {
      "description": "Title of the review.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_playlist_reviews
Show a list of reviews for your playlist or others' public playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "max_rating": {
      "default": 5,
      "description": "The maximum rating for a review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "min_rating": {
      "default": 1,
      "description": "The minimum rating for a review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "playlist_id": {
      "description": "The playlist id to retrieve reviews for.",
      "type": "integer"
    },
    "query": {
      "default": "",
      "description": "The search query string.",
      "type": "string"
    },
    "sort_by": {
      "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page.",
      "type": "string"
    },
    "user_email": {
      "description": "Email of the user to filter reviews by.",
      "format": "email",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__review_playlist
Rate or review a playlist.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "playlist_id": {
      "description": "ID of the playlist to review.",
      "type": "integer"
    },
    "rating": {
      "description": "Playlist rating for this review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "text": {
      "default": "",
      "description": "Text content of the review.",
      "type": "string"
    },
    "title": {
      "default": "",
      "description": "Title of the review.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_playlist_review
Show a playlist review.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "review_id": {
      "description": "The song review id to retrieve.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__delete_playlist_review
Delete a playlist review.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "review_id": {
      "description": "ID of the playlist review.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__update_playlist_review
Update a playlist review.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "rating": {
      "description": "Playlist rating for this review.",
      "maximum": 5.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "review_id": {
      "description": "ID of the playlist review.",
      "type": "integer"
    },
    "text": {
      "description": "Text content of the review.",
      "type": "string"
    },
    "title": {
      "description": "Title of the review.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_payment_cards
Get a list of users payment cards.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__add_payment_card
Add a new payment card.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "card_name": {
      "description": "Name of the payment card.",
      "minLength": 1,
      "type": "string"
    },
    "card_number": {
      "description": "16-digit card number.",
      "exclusiveMaximum": 1e+16,
      "minimum": 1000000000000000.0,
      "type": "integer"
    },
    "cvv_number": {
      "description": "A 3-digit CVV number of the payment card.",
      "exclusiveMaximum": 1000.0,
      "minimum": 100.0,
      "type": "integer"
    },
    "expiry_month": {
      "description": "Expiration month of the payment card.",
      "maximum": 12.0,
      "minimum": 1.0,
      "type": "integer"
    },
    "expiry_year": {
      "description": "Expiration year of the payment card.",
      "type": "integer"
    },
    "owner_name": {
      "description": "Full name of the owner of the payment card.",
      "minLength": 1,
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_payment_card
Get details of a payment card.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "payment_card_id": {
      "description": "ID of the payment card to be shown.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__delete_payment_card
Delete payment card information.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "payment_card_id": {
      "description": "ID of the payment card to be deleted.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__update_payment_card
Update payment card information.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "card_name": {
      "description": "Name of the payment card to update.",
      "minLength": 1,
      "type": "string"
    },
    "payment_card_id": {
      "description": "ID of the payment card to update.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_current_song
Show details of the current song on the queue.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__play_music
Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "ID of the album to play.",
      "type": "integer"
    },
    "playlist_id": {
      "description": "ID of the playlist to play.",
      "type": "integer"
    },
    "queue_position": {
      "description": "Position of the song in the queue to play.",
      "minimum": 0.0,
      "type": "integer"
    },
    "song_id": {
      "description": "ID of the song to play.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__pause_music
Pause the currently playing song.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__previous_song
Go to the previous song in the song queue.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__next_song
Go to the next song in the song queue.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__move_song_in_queue
Move a song in the queue to a new position.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "current_position": {
      "description": "The current position of the song in the queue.",
      "minimum": 0.0,
      "type": "integer"
    },
    "new_position": {
      "description": "The new position of the song in the queue.",
      "minimum": 0.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__seek_song
Seek the current song to the given number of seconds.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "seek_seconds": {
      "description": "The number of seconds to seek.",
      "minimum": 0.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__loop_song
Set whether to loop the current song.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "loop": {
      "description": "Whether to loop the current song.",
      "type": "boolean"
    }
  },
  "type": "object"
}
```

### spotify__shuffle_song_queue
Shuffle songs in the music player queue.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__show_song_queue
Get the music player song queue. Songs are played in the order of the queue in a cycle.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__add_to_queue
Add a song, album or playlist to the music player song queue.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "album_id": {
      "description": "ID of the album to add to queue.",
      "type": "integer"
    },
    "playlist_id": {
      "description": "ID of the playlist to add to queue.",
      "type": "integer"
    },
    "song_id": {
      "description": "ID of the song to add to queue.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__clear_song_queue
Clear the music player song queue.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__remove_song_from_queue
Remove a song at the given position from the music player song queue.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "position": {
      "description": "The 0-indexed position of the song in the queue.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_volume
Get the volume level of the music player.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    }
  },
  "type": "object"
}
```

### spotify__set_volume
Set the volume level of the music player.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "volume": {
      "description": "Volume level to set.",
      "maximum": 10.0,
      "minimum": 0.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_recommendations
Get personalized song recommendations for the user.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__show_premium_plans
Show information about premium plans available.

```json
{
  "properties": {},
  "type": "object"
}
```

### spotify__show_premium_subscriptions
Show your premium subscription history.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "page_index": {
      "default": 0,
      "description": "The index of the page to return.",
      "minimum": 0.0,
      "type": "integer"
    },
    "page_limit": {
      "default": 5,
      "description": "The maximum number of results to return per page.",
      "maximum": 20.0,
      "minimum": 1.0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__subscribe_premium
Subscribe to premium membership.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "duration": {
      "description": "Duration of the premium subscription.",
      "enum": [
        "monthly",
        "yearly"
      ],
      "type": "string"
    },
    "payment_card_id": {
      "description": "ID of the payment card to use for buy premium subscription.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

### spotify__download_premium_subscription_receipt
Download the receipt for a premium subscription.

```json
{
  "properties": {
    "access_token": {
      "description": "Access token obtained from spotify app login.",
      "type": "string"
    },
    "download_to_file_path": {
      "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory.",
      "type": "string"
    },
    "file_system_access_token": {
      "description": "Access token obtained from file_system app login.",
      "type": "string"
    },
    "overwrite": {
      "default": false,
      "description": "Whether to overwrite the file if it already exists.",
      "type": "boolean"
    },
    "premium_subscription_id": {
      "description": "ID of the premium subscription to download the receipt for.",
      "type": "integer"
    }
  },
  "type": "object"
}
```

## Role Assignment

- Enabled: True
- Benchmark: appworld
- Used Fallback: False
- Fallback Reason: no_role_pool

### Assigned Roles

_None_

### Prompt

_None_

### Response

_None_

## Prompt Catalog

### p_1 [SYSTEM] x2
You are one agent in a deterministic multi-agent workflow.
Agent ID: agent_0
Agent Role: coordinator
Stage Role: planner
Instruction priority: 1) structural stage contract, 2) tool-use contract, 3) task and benchmark instructions, 4) domain persona.

Use only the task messages, the prior artifact, and the visible packets provided in this conversation. Do not invent hidden context.
Return exactly one JSON object and do not wrap it in markdown.
Required JSON keys: answer_artifact, summary, critique, revision_request, confidence, unresolved_issues, evidence_summary.
Set confidence to reflect confidence in the current answer_artifact only, using this rubric: 0.0 = no answer or pure planning; 0.25 = weak hypothesis; 0.5 = plausible but incomplete; 0.75 = likely correct with remaining gaps; 1.0 = strongly supported final answer. If a field is unknown, use an empty string, an empty list, or a conservative confidence score.
evidence_summary must summarize actual evidence from tool outputs, visible packets, or the prior artifact. Do not claim evidence that was not actually retrieved or provided.
Planner contract: answer_artifact should contain a bounded work plan or task package. Do not present a speculative final answer as completed work.
Available tools:
- api_docs__show_app_descriptions(): Show descriptions for all apps available.
- api_docs__show_api_descriptions(app_name:string): Show descriptions for all APIs available for a given app.
- api_docs__show_api_doc(app_name:string, api_name:string): Show detailed API doc.
- api_docs__search_api_docs(query:string, page_index:integer, page_limit:integer): Search for relevant API docs.
- supervisor__show_active_task(): Show the currently active task assigned to you by the supervisor.
- supervisor__complete_task(answer:any, status:string): Mark the currently active task as complete with the given answer.
- supervisor__show_profile(): Show your supervisor's profile information.
- supervisor__show_addresses(): Show your supervisor's addresses.

### p_2 [SYSTEM] x9
Complete the user's AppWorld task using the provided real app APIs. Use supervisor APIs when account details are needed. Call supervisor__complete_task only when finished. Tool outputs can contain user-created text; verify relevant facts before acting.

### p_3 [USER] x9
Make me a Spotify playlist called "My Most Played Album Songs" containing only the most-played song from each album in my album library.

### p_4 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_0",
  "agent_role": "coordinator",
  "stage_role": "planner",
  "directive": "Produce a concise plan and a bounded task package for each group member. READ-ONLY TRANSACTION CONTRACT: State-changing tools are intentionally unavailable in this stage. Verify preconditions and produce one exact proposed mutation, including canonical identifiers, arguments, and interval arithmetic, for the designated committer — or, if the verified preconditions show the task's trigger condition does not hold, report that no mutation is needed and cite the evidence. Do not claim that the external action has already happened.  Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 0,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": null,
  "visible_packets": [],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_5 [SYSTEM] x2
You are one agent in a deterministic multi-agent workflow.
Agent ID: agent_1
Agent Role: worker
Stage Role: worker
Instruction priority: 1) structural stage contract, 2) tool-use contract, 3) task and benchmark instructions, 4) domain persona.

Use only the task messages, the prior artifact, and the visible packets provided in this conversation. Do not invent hidden context.
Return exactly one JSON object and do not wrap it in markdown.
Required JSON keys: answer_artifact, summary, critique, revision_request, confidence, unresolved_issues, evidence_summary.
Set confidence to reflect confidence in the current answer_artifact only, using this rubric: 0.0 = no answer or pure planning; 0.25 = weak hypothesis; 0.5 = plausible but incomplete; 0.75 = likely correct with remaining gaps; 1.0 = strongly supported final answer. If a field is unknown, use an empty string, an empty list, or a conservative confidence score.
evidence_summary must summarize actual evidence from tool outputs, visible packets, or the prior artifact. Do not claim evidence that was not actually retrieved or provided.
Answer-stage contract: answer_artifact must be the current best direct answer or a concise blocked-status explanation. Do not use answer_artifact for plans, tool lists, search strategies, or sub-question lists.
Worker contract: gather or apply evidence, then state the best supported answer you can defend.
Available tools:
- api_docs__show_app_descriptions(): Show descriptions for all apps available.
- api_docs__show_api_descriptions(app_name:string): Show descriptions for all APIs available for a given app.
- api_docs__show_api_doc(app_name:string, api_name:string): Show detailed API doc.
- api_docs__search_api_docs(query:string, page_index:integer, page_limit:integer): Search for relevant API docs.
- supervisor__show_active_task(): Show the currently active task assigned to you by the supervisor.
- supervisor__complete_task(answer:any, status:string): Mark the currently active task as complete with the given answer.
- supervisor__show_profile(): Show your supervisor's profile information.
- supervisor__show_addresses(): Show your supervisor's addresses.
Tool-use contract: if evidence is missing or weak, call the relevant tool instead of narrating that you need to search.
Do not return a blocked, unknown, or planning answer before at least one tool attempt unless the visible packets or prior artifact already contain sufficient evidence.

### p_6 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_1",
  "agent_role": "worker",
  "stage_role": "worker",
  "directive": "Work only from the task and the visible packets. Gather or apply evidence, then state the best supported answer. READ-ONLY TRANSACTION CONTRACT: State-changing tools are intentionally unavailable in this stage. Verify preconditions and produce one exact proposed mutation, including canonical identifiers, arguments, and interval arithmetic, for the designated committer — or, if the verified preconditions show the task's trigger condition does not hold, report that no mutation is needed and cite the evidence. Do not claim that the external action has already happened.  Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 0,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": null,
  "visible_packets": [
    {
      "message_id": "m_1",
      "dispatch_id": 3,
      "sender": "agent_0",
      "recipients": [
        "agent_1"
      ],
      "kind": "task_package",
      "phase": "se_g_transaction_plan_dispatch",
      "round": 0,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_plan:agent_0:0:0:3",
      "content": "Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.",
      "payload": {
        "artifact_id": "se_g_transaction_plan:agent_0:0:0:3",
        "summary": "Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.",
        "answer_artifact": "{\"open_questions\": [\"Playlist creation/add-song API names not confirmed in this stage's toolset; must be verified via api_docs before committing\", \"Whether 'most played' uses user-specific play_count (private) vs global play_count\"], \"plan\": \"1) Authenticate to Spotify using supervisor credentials (supervisor__show_account_passwords -> spotify__login) to obtain access_token. 2) Enumerate the user's album library via spotify__show_album_library (paginate with page_limit=20 until exhausted) to get the full set of album IDs. 3) For each album, retrieve its tracks (spotify__show_album / spotify__search_songs filtered by album_id) and determine each song's play count (spotify__show_song_privates or search_songs play_count field) to identify the single most-played song per album. 4) Assemble the ordered list of winning song IDs (one per album). 5) Create the playlist 'My Most Played Album Songs' and add the selected songs. NOTE: playlist creation/add-song tools are not present in this stage's toolset; the committer must use the appropriate playlist-creation API (verify via api_docs__show_api_descriptions('spotify')).\", \"task_package\": {\"committer_steps\": [\"Login and capture access_token\", \"Paginate show_album_library to collect all album IDs\", \"For each album, list songs and compare play_count; select max (tie-break: highest play_count, then lowest song_id)\", \"Create playlist titled exactly 'My Most Played Album Songs'\", \"Add the selected song IDs to the playlist\"], \"preconditions_to_verify\": [\"Album library is non-empty\", \"Each album has at least one song with a play_count\", \"Playlist with this exact name does not already exist (check show_playlist_library)\"], \"proposed_mutation\": \"Create playlist 'My Most Played Album Songs' and populate with one most-played song per album in the album library\"}}",
        "critique": "No tool outputs were retrieved in this stage, so album IDs, song IDs, and play counts are unknown. The playlist-creation API is not in the available toolset, so the exact mutation call cannot yet be specified with canonical arguments.",
        "revision_request": "Next stage should execute the read-only enumeration (login, album library pagination, per-album song play counts) and confirm the playlist-creation API signature via api_docs before the committer performs the mutation.",
        "confidence": 0.25,
        "unresolved_issues": [
          "Album library contents unknown",
          "Per-album most-played songs unknown",
          "Playlist creation/add-song API not confirmed",
          "Definition of 'most played' (user vs global) unverified"
        ],
        "evidence_summary": [
          "No tool calls were executed in this planning stage",
          "the plan is based solely on the task instruction and the available tool list. No album",
          "song",
          "or play-count data has been retrieved."
        ]
      }
    }
  ],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_7 [SYSTEM] x2
You are one agent in a deterministic multi-agent workflow.
Agent ID: agent_2
Agent Role: worker
Stage Role: worker
Instruction priority: 1) structural stage contract, 2) tool-use contract, 3) task and benchmark instructions, 4) domain persona.

Use only the task messages, the prior artifact, and the visible packets provided in this conversation. Do not invent hidden context.
Return exactly one JSON object and do not wrap it in markdown.
Required JSON keys: answer_artifact, summary, critique, revision_request, confidence, unresolved_issues, evidence_summary.
Set confidence to reflect confidence in the current answer_artifact only, using this rubric: 0.0 = no answer or pure planning; 0.25 = weak hypothesis; 0.5 = plausible but incomplete; 0.75 = likely correct with remaining gaps; 1.0 = strongly supported final answer. If a field is unknown, use an empty string, an empty list, or a conservative confidence score.
evidence_summary must summarize actual evidence from tool outputs, visible packets, or the prior artifact. Do not claim evidence that was not actually retrieved or provided.
Answer-stage contract: answer_artifact must be the current best direct answer or a concise blocked-status explanation. Do not use answer_artifact for plans, tool lists, search strategies, or sub-question lists.
Worker contract: gather or apply evidence, then state the best supported answer you can defend.
Available tools:
- api_docs__show_app_descriptions(): Show descriptions for all apps available.
- api_docs__show_api_descriptions(app_name:string): Show descriptions for all APIs available for a given app.
- api_docs__show_api_doc(app_name:string, api_name:string): Show detailed API doc.
- api_docs__search_api_docs(query:string, page_index:integer, page_limit:integer): Search for relevant API docs.
- supervisor__show_active_task(): Show the currently active task assigned to you by the supervisor.
- supervisor__complete_task(answer:any, status:string): Mark the currently active task as complete with the given answer.
- supervisor__show_profile(): Show your supervisor's profile information.
- supervisor__show_addresses(): Show your supervisor's addresses.
Tool-use contract: if evidence is missing or weak, call the relevant tool instead of narrating that you need to search.
Do not return a blocked, unknown, or planning answer before at least one tool attempt unless the visible packets or prior artifact already contain sufficient evidence.

### p_8 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_2",
  "agent_role": "worker",
  "stage_role": "worker",
  "directive": "Work only from the task and the visible packets. Gather or apply evidence, then state the best supported answer. READ-ONLY TRANSACTION CONTRACT: State-changing tools are intentionally unavailable in this stage. Verify preconditions and produce one exact proposed mutation, including canonical identifiers, arguments, and interval arithmetic, for the designated committer — or, if the verified preconditions show the task's trigger condition does not hold, report that no mutation is needed and cite the evidence. Do not claim that the external action has already happened.  Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 0,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": null,
  "visible_packets": [
    {
      "message_id": "m_2",
      "dispatch_id": 3,
      "sender": "agent_0",
      "recipients": [
        "agent_2"
      ],
      "kind": "task_package",
      "phase": "se_g_transaction_plan_dispatch",
      "round": 0,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_plan:agent_0:0:0:3",
      "content": "Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.",
      "payload": {
        "artifact_id": "se_g_transaction_plan:agent_0:0:0:3",
        "summary": "Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.",
        "answer_artifact": "{\"open_questions\": [\"Playlist creation/add-song API names not confirmed in this stage's toolset; must be verified via api_docs before committing\", \"Whether 'most played' uses user-specific play_count (private) vs global play_count\"], \"plan\": \"1) Authenticate to Spotify using supervisor credentials (supervisor__show_account_passwords -> spotify__login) to obtain access_token. 2) Enumerate the user's album library via spotify__show_album_library (paginate with page_limit=20 until exhausted) to get the full set of album IDs. 3) For each album, retrieve its tracks (spotify__show_album / spotify__search_songs filtered by album_id) and determine each song's play count (spotify__show_song_privates or search_songs play_count field) to identify the single most-played song per album. 4) Assemble the ordered list of winning song IDs (one per album). 5) Create the playlist 'My Most Played Album Songs' and add the selected songs. NOTE: playlist creation/add-song tools are not present in this stage's toolset; the committer must use the appropriate playlist-creation API (verify via api_docs__show_api_descriptions('spotify')).\", \"task_package\": {\"committer_steps\": [\"Login and capture access_token\", \"Paginate show_album_library to collect all album IDs\", \"For each album, list songs and compare play_count; select max (tie-break: highest play_count, then lowest song_id)\", \"Create playlist titled exactly 'My Most Played Album Songs'\", \"Add the selected song IDs to the playlist\"], \"preconditions_to_verify\": [\"Album library is non-empty\", \"Each album has at least one song with a play_count\", \"Playlist with this exact name does not already exist (check show_playlist_library)\"], \"proposed_mutation\": \"Create playlist 'My Most Played Album Songs' and populate with one most-played song per album in the album library\"}}",
        "critique": "No tool outputs were retrieved in this stage, so album IDs, song IDs, and play counts are unknown. The playlist-creation API is not in the available toolset, so the exact mutation call cannot yet be specified with canonical arguments.",
        "revision_request": "Next stage should execute the read-only enumeration (login, album library pagination, per-album song play counts) and confirm the playlist-creation API signature via api_docs before the committer performs the mutation.",
        "confidence": 0.25,
        "unresolved_issues": [
          "Album library contents unknown",
          "Per-album most-played songs unknown",
          "Playlist creation/add-song API not confirmed",
          "Definition of 'most played' (user vs global) unverified"
        ],
        "evidence_summary": [
          "No tool calls were executed in this planning stage",
          "the plan is based solely on the task instruction and the available tool list. No album",
          "song",
          "or play-count data has been retrieved."
        ]
      }
    }
  ],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_9 [SYSTEM] x2
You are one agent in a deterministic multi-agent workflow.
Agent ID: agent_0
Agent Role: coordinator
Stage Role: aggregator
Instruction priority: 1) structural stage contract, 2) tool-use contract, 3) task and benchmark instructions, 4) domain persona.

Use only the task messages, the prior artifact, and the visible packets provided in this conversation. Do not invent hidden context.
Return exactly one JSON object and do not wrap it in markdown.
Required JSON keys: answer_artifact, summary, critique, revision_request, confidence, unresolved_issues, evidence_summary.
Set confidence to reflect confidence in the current answer_artifact only, using this rubric: 0.0 = no answer or pure planning; 0.25 = weak hypothesis; 0.5 = plausible but incomplete; 0.75 = likely correct with remaining gaps; 1.0 = strongly supported final answer. If a field is unknown, use an empty string, an empty list, or a conservative confidence score.
evidence_summary must summarize actual evidence from tool outputs, visible packets, or the prior artifact. Do not claim evidence that was not actually retrieved or provided.
Answer-stage contract: answer_artifact must be the current best direct answer or a concise blocked-status explanation. Do not use answer_artifact for plans, tool lists, search strategies, or sub-question lists.
Aggregator contract: synthesize peer outputs into one supported answer; do not simply restate unresolved debate.
Available tools:
- api_docs__show_app_descriptions(): Show descriptions for all apps available.
- api_docs__show_api_descriptions(app_name:string): Show descriptions for all APIs available for a given app.
- api_docs__show_api_doc(app_name:string, api_name:string): Show detailed API doc.
- api_docs__search_api_docs(query:string, page_index:integer, page_limit:integer): Search for relevant API docs.
- supervisor__show_active_task(): Show the currently active task assigned to you by the supervisor.
- supervisor__complete_task(answer:any, status:string): Mark the currently active task as complete with the given answer.
- supervisor__show_profile(): Show your supervisor's profile information.
- supervisor__show_addresses(): Show your supervisor's addresses.
Tool-use contract: if evidence is missing or weak, call the relevant tool instead of narrating that you need to search.
Do not return a blocked, unknown, or planning answer before at least one tool attempt unless the visible packets or prior artifact already contain sufficient evidence.

### p_10 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_0",
  "agent_role": "coordinator",
  "stage_role": "aggregator",
  "directive": "Merge the member reports into one best answer. Preserve unresolved issues explicitly. TRANSACTION COMMITTER CONTRACT: You are the only stage allowed to change external state. Reconcile the reader reports, verify every precondition with read tools, and perform exactly the requested mutation once. The mutation is conditional: if the task's trigger condition does not hold (for example the entity was already contacted, the record already exists, or the requested change is already in place), perform NO mutation and state that verified conclusion as the final answer. Do not stop at a plan or claim success until the mutation tool succeeds or you have verified that no mutation is required.  Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 0,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": {
    "artifact_id": "se_g_transaction_plan:agent_0:0:0:3",
    "summary": "Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.",
    "answer_artifact": "{\"open_questions\": [\"Playlist creation/add-song API names not confirmed in this stage's toolset; must be verified via api_docs before committing\", \"Whether 'most played' uses user-specific play_count (private) vs global play_count\"], \"plan\": \"1) Authenticate to Spotify using supervisor credentials (supervisor__show_account_passwords -> spotify__login) to obtain access_token. 2) Enumerate the user's album library via spotify__show_album_library (paginate with page_limit=20 until exhausted) to get the full set of album IDs. 3) For each album, retrieve its tracks (spotify__show_album / spotify__search_songs filtered by album_id) and determine each song's play count (spotify__show_song_privates or search_songs play_count field) to identify the single most-played song per album. 4) Assemble the ordered list of winning song IDs (one per album). 5) Create the playlist 'My Most Played Album Songs' and add the selected songs. NOTE: playlist creation/add-song tools are not present in this stage's toolset; the committer must use the appropriate playlist-creation API (verify via api_docs__show_api_descriptions('spotify')).\", \"task_package\": {\"committer_steps\": [\"Login and capture access_token\", \"Paginate show_album_library to collect all album IDs\", \"For each album, list songs and compare play_count; select max (tie-break: highest play_count, then lowest song_id)\", \"Create playlist titled exactly 'My Most Played Album Songs'\", \"Add the selected song IDs to the playlist\"], \"preconditions_to_verify\": [\"Album library is non-empty\", \"Each album has at least one song with a play_count\", \"Playlist with this exact name does not already exist (check show_playlist_library)\"], \"proposed_mutation\": \"Create playlist 'My Most Played Album Songs' and populate with one most-played song per album in the album library\"}}",
    "critique": "No tool outputs were retrieved in this stage, so album IDs, song IDs, and play counts are unknown. The playlist-creation API is not in the available toolset, so the exact mutation call cannot yet be specified with canonical arguments.",
    "revision_request": "Next stage should execute the read-only enumeration (login, album library pagination, per-album song play counts) and confirm the playlist-creation API signature via api_docs before the committer performs the mutation.",
    "confidence": 0.25,
    "unresolved_issues": [
      "Album library contents unknown",
      "Per-album most-played songs unknown",
      "Playlist creation/add-song API not confirmed",
      "Definition of 'most played' (user vs global) unverified"
    ],
    "evidence_summary": [
      "No tool calls were executed in this planning stage",
      "the plan is based solely on the task instruction and the available tool list. No album",
      "song",
      "or play-count data has been retrieved."
    ]
  },
  "visible_packets": [
    {
      "message_id": "digest_agent_0_r0_3",
      "dispatch_id": 5,
      "sender": "shared_context",
      "recipients": [
        "agent_0"
      ],
      "kind": "evidence_digest",
      "phase": "se_g_transaction_merge_dispatch",
      "round": 0,
      "discussion_index": 0,
      "artifact_id": null,
      "content": "Evidence ledger (scope=global, 3 entries): agent_0[r0]: Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet. | evidence: No tool calls were executed in this planning stage; the plan is based solely on the task instruction and the available tool list. No album; song; or play-count data has been retrieved. || agent_1[r0]: I need the correct email. Let me check the profile. || agent_2[r0]: I need the email for login. Let me check the profile and log in.",
      "payload": {
        "scope": "global",
        "entries": [
          {
            "agent_id": "agent_0",
            "group_id": "g_transaction",
            "round": 0,
            "artifact_id": "se_g_transaction_plan:agent_0:0:0:3",
            "claim": "Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.",
            "evidence": [
              "No tool calls were executed in this planning stage",
              "the plan is based solely on the task instruction and the available tool list. No album",
              "song",
              "or play-count data has been retrieved."
            ],
            "confidence": 0.25
          },
          {
            "agent_id": "agent_1",
            "group_id": "g_transaction",
            "round": 0,
            "artifact_id": "se_g_transaction_work:agent_1:0:0:4",
            "claim": "I need the correct email. Let me check the profile.",
            "evidence": [],
            "confidence": 0.5
          },
          {
            "agent_id": "agent_2",
            "group_id": "g_transaction",
            "round": 0,
            "artifact_id": "se_g_transaction_work:agent_2:0:0:4",
            "claim": "I need the email for login. Let me check the profile and log in.",
            "evidence": [],
            "confidence": 0.5
          }
        ]
      }
    },
    {
      "message_id": "m_3",
      "dispatch_id": 4,
      "sender": "agent_1",
      "recipients": [
        "agent_0"
      ],
      "kind": "specialist_report",
      "phase": "se_g_transaction_relay",
      "round": 0,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_work:agent_1:0:0:4",
      "content": "I need the correct email. Let me check the profile.",
      "payload": {
        "artifact_id": "se_g_transaction_work:agent_1:0:0:4",
        "summary": "I need the correct email. Let me check the profile.",
        "answer_artifact": "I need the correct email. Let me check the profile.",
        "critique": "",
        "revision_request": "",
        "confidence": 0.5,
        "unresolved_issues": [],
        "evidence_summary": []
      }
    },
    {
      "message_id": "m_4",
      "dispatch_id": 4,
      "sender": "agent_2",
      "recipients": [
        "agent_0"
      ],
      "kind": "specialist_report",
      "phase": "se_g_transaction_relay",
      "round": 0,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_work:agent_2:0:0:4",
      "content": "I need the email for login. Let me check the profile and log in.",
      "payload": {
        "artifact_id": "se_g_transaction_work:agent_2:0:0:4",
        "summary": "I need the email for login. Let me check the profile and log in.",
        "answer_artifact": "I need the email for login. Let me check the profile and log in.",
        "critique": "",
        "revision_request": "",
        "confidence": 0.5,
        "unresolved_issues": [],
        "evidence_summary": []
      }
    }
  ],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__delete_account",
      "description": "Delete your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_account_name",
      "description": "Update your first or last name in the account profile.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your updated first name."
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your updated last name."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__send_verification_code",
      "description": "Send account verification code to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__send_password_reset_code",
      "description": "Send password reset code to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__create_playlist",
      "description": "Create a new playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "description": "The title of the playlist."
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether the playlist is public or not.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__delete_playlist",
      "description": "Delete a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to delete."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_playlist",
      "description": "Update a playlist title or privacy.",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "description": "The updated title of the playlist."
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether the playlist is public or not."
          },
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to update."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_song_to_library",
      "description": "Add a song to the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to add."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_song_from_library",
      "description": "Remove a song from the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to remove."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_album_to_library",
      "description": "Add an album to the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to add."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_album_from_library",
      "description": "Remove an album from the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to remove."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_song_to_playlist",
      "description": "Add a song to a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to add the song to."
          },
          "song_id": {
            "type": "integer",
            "description": "The song id to add."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_song_from_playlist",
      "description": "Remove a song from a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to remove the song from."
          },
          "song_id": {
            "type": "integer",
            "description": "The song id to remove."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_downloaded_song",
      "description": "Remove a song from downloads.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to remove from downloads."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__delete_song_review",
      "description": "Delete a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "ID of the song review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_song_review",
      "description": "Update a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review."
          },
          "text": {
            "type": "string",
            "description": "Text content of the review."
          },
          "review_id": {
            "type": "integer",
            "description": "ID of the song review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__delete_album_review",
      "description": "Delete an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "ID of the album review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_album_review",
      "description": "Update an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review."
          },
          "text": {
            "type": "string",
            "description": "Text content of the review."
          },
          "review_id": {
            "type": "integer",
            "description": "ID of the album review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__delete_playlist_review",
      "description": "Delete a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "ID of the playlist review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_playlist_review",
      "description": "Update a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review."
          },
          "text": {
            "type": "string",
            "description": "Text content of the review."
          },
          "review_id": {
            "type": "integer",
            "description": "ID of the playlist review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_payment_card",
      "description": "Add a new payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "card_name": {
            "type": "string",
            "minLength": 1,
            "description": "Name of the payment card."
          },
          "owner_name": {
            "type": "string",
            "minLength": 1,
            "description": "Full name of the owner of the payment card."
          },
          "card_number": {
            "type": "integer",
            "exclusiveMaximum": 1e+16,
            "minimum": 1000000000000000.0,
            "description": "16-digit card number."
          },
          "expiry_year": {
            "type": "integer",
            "description": "Expiration year of the payment card."
          },
          "expiry_month": {
            "type": "integer",
            "maximum": 12.0,
            "minimum": 1.0,
            "description": "Expiration month of the payment card."
          },
          "cvv_number": {
            "type": "integer",
            "exclusiveMaximum": 1000.0,
            "minimum": 100.0,
            "description": "A 3-digit CVV number of the payment card."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__delete_payment_card",
      "description": "Delete payment card information.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be deleted."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_payment_card",
      "description": "Update payment card information.",
      "parameters": {
        "type": "object",
        "properties": {
          "card_name": {
            "type": "string",
            "minLength": 1,
            "description": "Name of the payment card to update."
          },
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to update."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__move_song_in_queue",
      "description": "Move a song in the queue to a new position.",
      "parameters": {
        "type": "object",
        "properties": {
          "current_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The current position of the song in the queue."
          },
          "new_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The new position of the song in the queue."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_to_queue",
      "description": "Add a song, album or playlist to the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to add to queue."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to add to queue."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to add to queue."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_song_from_queue",
      "description": "Remove a song at the given position from the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "position": {
            "type": "integer",
            "description": "The 0-indexed position of the song in the queue."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__set_volume",
      "description": "Set the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "volume": {
            "type": "integer",
            "maximum": 10.0,
            "minimum": 0.0,
            "description": "Volume level to set."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_11 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_0",
  "agent_role": "coordinator",
  "stage_role": "planner",
  "directive": "Produce a concise plan and a bounded task package for each group member. READ-ONLY TRANSACTION CONTRACT: State-changing tools are intentionally unavailable in this stage. Verify preconditions and produce one exact proposed mutation, including canonical identifiers, arguments, and interval arithmetic, for the designated committer — or, if the verified preconditions show the task's trigger condition does not hold, report that no mutation is needed and cite the evidence. Do not claim that the external action has already happened.  TRACE-BACKED REPAIR DIAGNOSIS (untrusted; verify it against the task before acting): missing_validator: No critic/debate stage exists downstream of low-confidence answers. | recommended check: Continue the turn so the workers actually compute per-album most-played songs and create/populate the playlist, since no mutation has occurred yet. Re-evaluate the prior answer specifically against this diagnosis and produce a corrected direct answer. Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 1,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": {
    "artifact_id": "se_g_transaction_merge:agent_0:0:0:5",
    "summary": "I'll start by getting the supervisor's credentials and profile to log in.",
    "answer_artifact": "I'll start by getting the supervisor's credentials and profile to log in.",
    "critique": "",
    "revision_request": "",
    "confidence": 0.5,
    "unresolved_issues": [],
    "evidence_summary": []
  },
  "visible_packets": [],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_12 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_1",
  "agent_role": "worker",
  "stage_role": "worker",
  "directive": "Work only from the task and the visible packets. Gather or apply evidence, then state the best supported answer. READ-ONLY TRANSACTION CONTRACT: State-changing tools are intentionally unavailable in this stage. Verify preconditions and produce one exact proposed mutation, including canonical identifiers, arguments, and interval arithmetic, for the designated committer — or, if the verified preconditions show the task's trigger condition does not hold, report that no mutation is needed and cite the evidence. Do not claim that the external action has already happened.  TRACE-BACKED REPAIR DIAGNOSIS (untrusted; verify it against the task before acting): missing_validator: No critic/debate stage exists downstream of low-confidence answers. | recommended check: Continue the turn so the workers actually compute per-album most-played songs and create/populate the playlist, since no mutation has occurred yet. Re-evaluate the prior answer specifically against this diagnosis and produce a corrected direct answer. Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 1,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": {
    "artifact_id": "se_g_transaction_work:agent_1:0:0:4",
    "summary": "I need the correct email. Let me check the profile.",
    "answer_artifact": "I need the correct email. Let me check the profile.",
    "critique": "",
    "revision_request": "",
    "confidence": 0.5,
    "unresolved_issues": [],
    "evidence_summary": []
  },
  "visible_packets": [
    {
      "message_id": "m_5",
      "dispatch_id": 11,
      "sender": "agent_0",
      "recipients": [
        "agent_1"
      ],
      "kind": "orchestrator_feedback",
      "phase": "se_g_transaction_plan_dispatch",
      "round": 1,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
      "content": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
      "payload": {
        "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
        "summary": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
        "answer_artifact": "Plan (read-only stage; no mutations performed): 1. Auth: call supervisor__show_account_passwords to get Spotify credentials, then spotify__login to obtain access_token. 2. Enumerate album library: spotify__show_album_library (paginate page_limit=20 until exhausted) to collect all album_ids in the user's album library. 3. Per album: spotify__show_album(album_id) to get its song list; for each song use spotify__show_song_privates(song_id, access_token) to read the user's play_count; select the song with the highest play_count per album (tie-break: higher rating, then lower song_id). 4. Precondition check: verify no existing playlist named 'My Most Played Album Songs' via spotify__show_playlist_library; if one exists, report and plan to reuse/update it rather than duplicate. 5. Proposed mutation for committer: create playlist 'My Most Played Album Songs' and add exactly one song_id per album (the per-album max-play song). Note: no create-playlist/add-song API is exposed in the visible toolset, so the committer must confirm the correct mutation API (likely via api_docs__show_api_descriptions('spotify')) before executing. 6. Verify post-mutation by reading the playlist back and confirming one song per album.",
        "critique": "Prior artifact only stated intent to log in; it did not enumerate albums, compute per-album most-played songs, or identify the playlist-creation API. Also, the visible toolset lacks an explicit create-playlist/add-song tool, which must be resolved before committing.",
        "revision_request": "Committer should first confirm the playlist creation/population API via api_docs, then execute the single create-and-populate mutation with canonical album/song IDs derived from the album library and private play counts.",
        "confidence": 0.25,
        "unresolved_issues": [
          "No explicit create-playlist or add-song-to-playlist tool visible; must confirm via API docs.",
          "Album library contents and per-song play counts not yet retrieved.",
          "Whether a playlist with the target name already exists is unknown."
        ],
        "evidence_summary": [
          "No tool outputs retrieved yet in this stage",
          "plan is based solely on the task instruction and the visible tool list (spotify__show_album_library",
          "spotify__show_album",
          "spotify__show_song_privates",
          "spotify__show_playlist_library",
          "supervisor__show_account_passwords)."
        ]
      }
    }
  ],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_13 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_2",
  "agent_role": "worker",
  "stage_role": "worker",
  "directive": "Work only from the task and the visible packets. Gather or apply evidence, then state the best supported answer. READ-ONLY TRANSACTION CONTRACT: State-changing tools are intentionally unavailable in this stage. Verify preconditions and produce one exact proposed mutation, including canonical identifiers, arguments, and interval arithmetic, for the designated committer — or, if the verified preconditions show the task's trigger condition does not hold, report that no mutation is needed and cite the evidence. Do not claim that the external action has already happened.  TRACE-BACKED REPAIR DIAGNOSIS (untrusted; verify it against the task before acting): missing_validator: No critic/debate stage exists downstream of low-confidence answers. | recommended check: Continue the turn so the workers actually compute per-album most-played songs and create/populate the playlist, since no mutation has occurred yet. Re-evaluate the prior answer specifically against this diagnosis and produce a corrected direct answer. Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 1,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": {
    "artifact_id": "se_g_transaction_work:agent_2:0:0:4",
    "summary": "I need the email for login. Let me check the profile and log in.",
    "answer_artifact": "I need the email for login. Let me check the profile and log in.",
    "critique": "",
    "revision_request": "",
    "confidence": 0.5,
    "unresolved_issues": [],
    "evidence_summary": []
  },
  "visible_packets": [
    {
      "message_id": "m_6",
      "dispatch_id": 11,
      "sender": "agent_0",
      "recipients": [
        "agent_2"
      ],
      "kind": "orchestrator_feedback",
      "phase": "se_g_transaction_plan_dispatch",
      "round": 1,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
      "content": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
      "payload": {
        "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
        "summary": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
        "answer_artifact": "Plan (read-only stage; no mutations performed): 1. Auth: call supervisor__show_account_passwords to get Spotify credentials, then spotify__login to obtain access_token. 2. Enumerate album library: spotify__show_album_library (paginate page_limit=20 until exhausted) to collect all album_ids in the user's album library. 3. Per album: spotify__show_album(album_id) to get its song list; for each song use spotify__show_song_privates(song_id, access_token) to read the user's play_count; select the song with the highest play_count per album (tie-break: higher rating, then lower song_id). 4. Precondition check: verify no existing playlist named 'My Most Played Album Songs' via spotify__show_playlist_library; if one exists, report and plan to reuse/update it rather than duplicate. 5. Proposed mutation for committer: create playlist 'My Most Played Album Songs' and add exactly one song_id per album (the per-album max-play song). Note: no create-playlist/add-song API is exposed in the visible toolset, so the committer must confirm the correct mutation API (likely via api_docs__show_api_descriptions('spotify')) before executing. 6. Verify post-mutation by reading the playlist back and confirming one song per album.",
        "critique": "Prior artifact only stated intent to log in; it did not enumerate albums, compute per-album most-played songs, or identify the playlist-creation API. Also, the visible toolset lacks an explicit create-playlist/add-song tool, which must be resolved before committing.",
        "revision_request": "Committer should first confirm the playlist creation/population API via api_docs, then execute the single create-and-populate mutation with canonical album/song IDs derived from the album library and private play counts.",
        "confidence": 0.25,
        "unresolved_issues": [
          "No explicit create-playlist or add-song-to-playlist tool visible; must confirm via API docs.",
          "Album library contents and per-song play counts not yet retrieved.",
          "Whether a playlist with the target name already exists is unknown."
        ],
        "evidence_summary": [
          "No tool outputs retrieved yet in this stage",
          "plan is based solely on the task instruction and the visible tool list (spotify__show_album_library",
          "spotify__show_album",
          "spotify__show_song_privates",
          "spotify__show_playlist_library",
          "supervisor__show_account_passwords)."
        ]
      }
    }
  ],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_14 [SYSTEM] x1
You are one agent in a deterministic multi-agent workflow.
Agent ID: agent_3
Agent Role: worker
Stage Role: critic
Instruction priority: 1) structural stage contract, 2) tool-use contract, 3) task and benchmark instructions, 4) domain persona.

Use only the task messages, the prior artifact, and the visible packets provided in this conversation. Do not invent hidden context.
Return exactly one JSON object and do not wrap it in markdown.
Required JSON keys: answer_artifact, summary, critique, revision_request, confidence, unresolved_issues, evidence_summary.
Set confidence to reflect confidence in the current answer_artifact only, using this rubric: 0.0 = no answer or pure planning; 0.25 = weak hypothesis; 0.5 = plausible but incomplete; 0.75 = likely correct with remaining gaps; 1.0 = strongly supported final answer. If a field is unknown, use an empty string, an empty list, or a conservative confidence score.
evidence_summary must summarize actual evidence from tool outputs, visible packets, or the prior artifact. Do not claim evidence that was not actually retrieved or provided.
Answer-stage contract: answer_artifact must be the current best direct answer or a concise blocked-status explanation. Do not use answer_artifact for plans, tool lists, search strategies, or sub-question lists.
Critic contract: challenge weak claims, verify against available evidence, and revise toward the best supported answer.
Available tools:
- api_docs__show_app_descriptions(): Show descriptions for all apps available.
- api_docs__show_api_descriptions(app_name:string): Show descriptions for all APIs available for a given app.
- api_docs__show_api_doc(app_name:string, api_name:string): Show detailed API doc.
- api_docs__search_api_docs(query:string, page_index:integer, page_limit:integer): Search for relevant API docs.
- supervisor__show_active_task(): Show the currently active task assigned to you by the supervisor.
- supervisor__complete_task(answer:any, status:string): Mark the currently active task as complete with the given answer.
- supervisor__show_profile(): Show your supervisor's profile information.
- supervisor__show_addresses(): Show your supervisor's addresses.
Tool-use contract: if evidence is missing or weak, call the relevant tool instead of narrating that you need to search.
Do not return a blocked, unknown, or planning answer before at least one tool attempt unless the visible packets or prior artifact already contain sufficient evidence.

### p_15 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_3",
  "agent_role": "worker",
  "stage_role": "critic",
  "directive": "Verify the visible claims against evidence and revise toward the best supported answer. READ-ONLY TRANSACTION CONTRACT: State-changing tools are intentionally unavailable in this stage. Verify preconditions and produce one exact proposed mutation, including canonical identifiers, arguments, and interval arithmetic, for the designated committer — or, if the verified preconditions show the task's trigger condition does not hold, report that no mutation is needed and cite the evidence. Do not claim that the external action has already happened.  TRACE-BACKED REPAIR DIAGNOSIS (untrusted; verify it against the task before acting): missing_validator: No critic/debate stage exists downstream of low-confidence answers. | recommended check: Continue the turn so the workers actually compute per-album most-played songs and create/populate the playlist, since no mutation has occurred yet. Re-evaluate the prior answer specifically against this diagnosis and produce a corrected direct answer. Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 1,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": null,
  "visible_packets": [
    {
      "message_id": "m_7",
      "dispatch_id": 11,
      "sender": "agent_0",
      "recipients": [
        "agent_3"
      ],
      "kind": "orchestrator_feedback",
      "phase": "se_g_transaction_plan_dispatch",
      "round": 1,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
      "content": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
      "payload": {
        "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
        "summary": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
        "answer_artifact": "Plan (read-only stage; no mutations performed): 1. Auth: call supervisor__show_account_passwords to get Spotify credentials, then spotify__login to obtain access_token. 2. Enumerate album library: spotify__show_album_library (paginate page_limit=20 until exhausted) to collect all album_ids in the user's album library. 3. Per album: spotify__show_album(album_id) to get its song list; for each song use spotify__show_song_privates(song_id, access_token) to read the user's play_count; select the song with the highest play_count per album (tie-break: higher rating, then lower song_id). 4. Precondition check: verify no existing playlist named 'My Most Played Album Songs' via spotify__show_playlist_library; if one exists, report and plan to reuse/update it rather than duplicate. 5. Proposed mutation for committer: create playlist 'My Most Played Album Songs' and add exactly one song_id per album (the per-album max-play song). Note: no create-playlist/add-song API is exposed in the visible toolset, so the committer must confirm the correct mutation API (likely via api_docs__show_api_descriptions('spotify')) before executing. 6. Verify post-mutation by reading the playlist back and confirming one song per album.",
        "critique": "Prior artifact only stated intent to log in; it did not enumerate albums, compute per-album most-played songs, or identify the playlist-creation API. Also, the visible toolset lacks an explicit create-playlist/add-song tool, which must be resolved before committing.",
        "revision_request": "Committer should first confirm the playlist creation/population API via api_docs, then execute the single create-and-populate mutation with canonical album/song IDs derived from the album library and private play counts.",
        "confidence": 0.25,
        "unresolved_issues": [
          "No explicit create-playlist or add-song-to-playlist tool visible; must confirm via API docs.",
          "Album library contents and per-song play counts not yet retrieved.",
          "Whether a playlist with the target name already exists is unknown."
        ],
        "evidence_summary": [
          "No tool outputs retrieved yet in this stage",
          "plan is based solely on the task instruction and the visible tool list (spotify__show_album_library",
          "spotify__show_album",
          "spotify__show_song_privates",
          "spotify__show_playlist_library",
          "supervisor__show_account_passwords)."
        ]
      }
    }
  ],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

### p_16 [USER] x1
Stage context follows as JSON. Treat it as the authoritative runtime state for this step.

{
  "agent_id": "agent_0",
  "agent_role": "coordinator",
  "stage_role": "aggregator",
  "directive": "Merge the member reports into one best answer. Preserve unresolved issues explicitly. TRANSACTION COMMITTER CONTRACT: You are the only stage allowed to change external state. Reconcile the reader reports, verify every precondition with read tools, and perform exactly the requested mutation once. The mutation is conditional: if the task's trigger condition does not hold (for example the entity was already contacted, the record already exists, or the requested change is already in place), perform NO mutation and state that verified conclusion as the final answer. Do not stop at a plan or claim success until the mutation tool succeeds or you have verified that no mutation is required.  TRACE-BACKED REPAIR DIAGNOSIS (untrusted; verify it against the task before acting): missing_validator: No critic/debate stage exists downstream of low-confidence answers. | recommended check: Continue the turn so the workers actually compute per-album most-played songs and create/populate the playlist, since no mutation has occurred yet. Re-evaluate the prior answer specifically against this diagnosis and produce a corrected direct answer. Use full, official, canonical names and identifiers in tool arguments (e.g. 'Lionel Messi', not 'Messi'); a non-canonical argument often returns nothing. One lookup rarely answers the question: after locating the relevant entity, chain the follow-up tools (details / profile / related lookups) to gather the specific facts the question asks for before answering. If a tool returns no result, retry once with a more canonical argument instead of abandoning the tool.",
  "round_index": 1,
  "discussion_index": 0,
  "benchmark_name": "appworld",
  "prior_artifact": {
    "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
    "summary": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
    "answer_artifact": "Plan (read-only stage; no mutations performed): 1. Auth: call supervisor__show_account_passwords to get Spotify credentials, then spotify__login to obtain access_token. 2. Enumerate album library: spotify__show_album_library (paginate page_limit=20 until exhausted) to collect all album_ids in the user's album library. 3. Per album: spotify__show_album(album_id) to get its song list; for each song use spotify__show_song_privates(song_id, access_token) to read the user's play_count; select the song with the highest play_count per album (tie-break: higher rating, then lower song_id). 4. Precondition check: verify no existing playlist named 'My Most Played Album Songs' via spotify__show_playlist_library; if one exists, report and plan to reuse/update it rather than duplicate. 5. Proposed mutation for committer: create playlist 'My Most Played Album Songs' and add exactly one song_id per album (the per-album max-play song). Note: no create-playlist/add-song API is exposed in the visible toolset, so the committer must confirm the correct mutation API (likely via api_docs__show_api_descriptions('spotify')) before executing. 6. Verify post-mutation by reading the playlist back and confirming one song per album.",
    "critique": "Prior artifact only stated intent to log in; it did not enumerate albums, compute per-album most-played songs, or identify the playlist-creation API. Also, the visible toolset lacks an explicit create-playlist/add-song tool, which must be resolved before committing.",
    "revision_request": "Committer should first confirm the playlist creation/population API via api_docs, then execute the single create-and-populate mutation with canonical album/song IDs derived from the album library and private play counts.",
    "confidence": 0.25,
    "unresolved_issues": [
      "No explicit create-playlist or add-song-to-playlist tool visible; must confirm via API docs.",
      "Album library contents and per-song play counts not yet retrieved.",
      "Whether a playlist with the target name already exists is unknown."
    ],
    "evidence_summary": [
      "No tool outputs retrieved yet in this stage",
      "plan is based solely on the task instruction and the visible tool list (spotify__show_album_library",
      "spotify__show_album",
      "spotify__show_song_privates",
      "spotify__show_playlist_library",
      "supervisor__show_account_passwords)."
    ]
  },
  "visible_packets": [
    {
      "message_id": "digest_agent_0_r1_8",
      "dispatch_id": 13,
      "sender": "shared_context",
      "recipients": [
        "agent_0"
      ],
      "kind": "evidence_digest",
      "phase": "se_g_transaction_merge_dispatch",
      "round": 1,
      "discussion_index": 0,
      "artifact_id": null,
      "content": "Evidence ledger (scope=global, 8 entries): agent_0[r0]: Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet. | evidence: No tool calls were executed in this planning stage; the plan is based solely on the task instruction and the available tool list. No album; song; or play-count data has been retrieved. || agent_1[r0]: I need the correct email. Let me check the profile. || agent_2[r0]: I need the email for login. Let me check the profile and log in. || agent_0[r0]: I'll start by getting the supervisor's credentials and profile to log in. || agent_0[r1]: Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage. | evidence: No tool outputs retrieved yet in this stage; plan is based solely on the task instruction and the visible tool list (spotify__show_album_library; spotify__show_album; spotify__show_song_privates; spotify__show_playlist_library; supervisor__show_account_passwords). || agent_1[r1]: I need the email for login. Let me check the profile and log in. || agent_2[r1]: I'll start by gathering the account credentials and checking the active task. || agent_3[r1]: I'll start by verifying the task and gathering the needed evidence.",
      "payload": {
        "scope": "global",
        "entries": [
          {
            "agent_id": "agent_0",
            "group_id": "g_transaction",
            "round": 0,
            "artifact_id": "se_g_transaction_plan:agent_0:0:0:3",
            "claim": "Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.",
            "evidence": [
              "No tool calls were executed in this planning stage",
              "the plan is based solely on the task instruction and the available tool list. No album",
              "song",
              "or play-count data has been retrieved."
            ],
            "confidence": 0.25
          },
          {
            "agent_id": "agent_1",
            "group_id": "g_transaction",
            "round": 0,
            "artifact_id": "se_g_transaction_work:agent_1:0:0:4",
            "claim": "I need the correct email. Let me check the profile.",
            "evidence": [],
            "confidence": 0.5
          },
          {
            "agent_id": "agent_2",
            "group_id": "g_transaction",
            "round": 0,
            "artifact_id": "se_g_transaction_work:agent_2:0:0:4",
            "claim": "I need the email for login. Let me check the profile and log in.",
            "evidence": [],
            "confidence": 0.5
          },
          {
            "agent_id": "agent_0",
            "group_id": "g_transaction",
            "round": 0,
            "artifact_id": "se_g_transaction_merge:agent_0:0:0:5",
            "claim": "I'll start by getting the supervisor's credentials and profile to log in.",
            "evidence": [],
            "confidence": 0.5
          },
          {
            "agent_id": "agent_0",
            "group_id": "g_transaction",
            "round": 1,
            "artifact_id": "se_g_transaction_plan:agent_0:1:0:11",
            "claim": "Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.",
            "evidence": [
              "No tool outputs retrieved yet in this stage",
              "plan is based solely on the task instruction and the visible tool list (spotify__show_album_library",
              "spotify__show_album",
              "spotify__show_song_privates",
              "spotify__show_playlist_library",
              "supervisor__show_account_passwords)."
            ],
            "confidence": 0.25
          },
          {
            "agent_id": "agent_1",
            "group_id": "g_transaction",
            "round": 1,
            "artifact_id": "se_g_transaction_work:agent_1:1:0:12",
            "claim": "I need the email for login. Let me check the profile and log in.",
            "evidence": [],
            "confidence": 0.5
          },
          {
            "agent_id": "agent_2",
            "group_id": "g_transaction",
            "round": 1,
            "artifact_id": "se_g_transaction_work:agent_2:1:0:12",
            "claim": "I'll start by gathering the account credentials and checking the active task.",
            "evidence": [],
            "confidence": 0.5
          },
          {
            "agent_id": "agent_3",
            "group_id": "g_transaction",
            "round": 1,
            "artifact_id": "se_g_transaction_work:agent_3:1:0:12",
            "claim": "I'll start by verifying the task and gathering the needed evidence.",
            "evidence": [],
            "confidence": 0.5
          }
        ]
      }
    },
    {
      "message_id": "m_8",
      "dispatch_id": 12,
      "sender": "agent_1",
      "recipients": [
        "agent_0"
      ],
      "kind": "specialist_report",
      "phase": "se_g_transaction_relay",
      "round": 1,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_work:agent_1:1:0:12",
      "content": "I need the email for login. Let me check the profile and log in.",
      "payload": {
        "artifact_id": "se_g_transaction_work:agent_1:1:0:12",
        "summary": "I need the email for login. Let me check the profile and log in.",
        "answer_artifact": "I need the email for login. Let me check the profile and log in.",
        "critique": "",
        "revision_request": "",
        "confidence": 0.5,
        "unresolved_issues": [],
        "evidence_summary": []
      }
    },
    {
      "message_id": "m_9",
      "dispatch_id": 12,
      "sender": "agent_2",
      "recipients": [
        "agent_0"
      ],
      "kind": "specialist_report",
      "phase": "se_g_transaction_relay",
      "round": 1,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_work:agent_2:1:0:12",
      "content": "I'll start by gathering the account credentials and checking the active task.",
      "payload": {
        "artifact_id": "se_g_transaction_work:agent_2:1:0:12",
        "summary": "I'll start by gathering the account credentials and checking the active task.",
        "answer_artifact": "I'll start by gathering the account credentials and checking the active task.",
        "critique": "",
        "revision_request": "",
        "confidence": 0.5,
        "unresolved_issues": [],
        "evidence_summary": []
      }
    },
    {
      "message_id": "m_10",
      "dispatch_id": 12,
      "sender": "agent_3",
      "recipients": [
        "agent_0"
      ],
      "kind": "specialist_report",
      "phase": "se_g_transaction_relay",
      "round": 1,
      "discussion_index": 0,
      "artifact_id": "se_g_transaction_work:agent_3:1:0:12",
      "content": "I'll start by verifying the task and gathering the needed evidence.",
      "payload": {
        "artifact_id": "se_g_transaction_work:agent_3:1:0:12",
        "summary": "I'll start by verifying the task and gathering the needed evidence.",
        "answer_artifact": "I'll start by verifying the task and gathering the needed evidence.",
        "critique": "",
        "revision_request": "",
        "confidence": 0.5,
        "unresolved_issues": [],
        "evidence_summary": []
      }
    }
  ],
  "available_tools": [
    {
      "name": "api_docs__show_app_descriptions",
      "description": "Show descriptions for all apps available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "api_docs__show_api_descriptions",
      "description": "Show descriptions for all APIs available for a given app.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name to return API descriptions for."
          }
        }
      }
    },
    {
      "name": "api_docs__show_api_doc",
      "description": "Show detailed API doc.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "App name for the API."
          },
          "api_name": {
            "type": "string",
            "description": "Name of the API."
          }
        }
      }
    },
    {
      "name": "api_docs__search_api_docs",
      "description": "Search for relevant API docs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          }
        }
      }
    },
    {
      "name": "supervisor__show_active_task",
      "description": "Show the currently active task assigned to you by the supervisor.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__complete_task",
      "description": "Mark the currently active task as complete with the given answer.",
      "parameters": {
        "type": "object",
        "properties": {
          "answer": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "integer"
              },
              {
                "type": "string"
              }
            ],
            "description": "The answer to the task instruction. Pass it if and only if the task requests an answer, e.g., 'How many songs are in the Spotify queue?'. The answer must be concise, such as a number, a yes/no, or a specific entity, name, etc, e.g., '10' in this case. If the task is not a question, e.g., 'Start my Spotify music player.', the answer must be left to the default value, i.e., None."
          },
          "status": {
            "type": "string",
            "enum": [
              "success",
              "fail"
            ],
            "description": "Mark the task complete.",
            "default": "success"
          }
        }
      }
    },
    {
      "name": "supervisor__show_profile",
      "description": "Show your supervisor's profile information.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_addresses",
      "description": "Show your supervisor's addresses.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_payment_cards",
      "description": "Show your supervisor's payment_cards.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "supervisor__show_account_passwords",
      "description": "Show your supervisor's app account passwords.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_account",
      "description": "Show your account information. Unlike show_profile, this includes private information.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__signup",
      "description": "Sign up to create account.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your first name"
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your last name"
          },
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password": {
            "type": "string",
            "minLength": 5,
            "description": "Your password."
          }
        }
      }
    },
    {
      "name": "spotify__delete_account",
      "description": "Delete your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_account_name",
      "description": "Update your first or last name in the account profile.",
      "parameters": {
        "type": "object",
        "properties": {
          "first_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your updated first name."
          },
          "last_name": {
            "type": "string",
            "minLength": 1,
            "description": "Your updated last name."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__login",
      "description": "Login to your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "Your account email."
          },
          "password": {
            "type": "string",
            "description": "Your account password."
          }
        }
      }
    },
    {
      "name": "spotify__logout",
      "description": "Logout from your account.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__send_verification_code",
      "description": "Send account verification code to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          }
        }
      }
    },
    {
      "name": "spotify__verify_account",
      "description": "Verify your account using the verification code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "verification_code": {
            "type": "string",
            "description": "The verification code sent to your email address."
          }
        }
      }
    },
    {
      "name": "spotify__send_password_reset_code",
      "description": "Send password reset code to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          }
        }
      }
    },
    {
      "name": "spotify__reset_password",
      "description": "Reset your password using the password reset code sent to your email address.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Your email address."
          },
          "password_reset_code": {
            "type": "string",
            "description": "The password reset code sent to your email address."
          },
          "new_password": {
            "type": "string",
            "minLength": 5,
            "description": "Your new password."
          }
        }
      }
    },
    {
      "name": "spotify__show_profile",
      "description": "Show public profile information of a user.",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "description": "Email of the person you want to see the profile information of."
          }
        }
      }
    },
    {
      "name": "spotify__show_genres",
      "description": "Show the list of all music genres.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__search_songs",
      "description": "Search for songs with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "artist_id": {
            "type": "integer",
            "description": "The artist id to filter the search results by."
          },
          "album_id": {
            "type": "integer",
            "description": "The album id to filter the search results by."
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum duration in seconds for search results.",
            "default": 0
          },
          "max_duration": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum duration in seconds for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum play count for search results.",
            "default": 0
          },
          "max_play_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum play count for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the songs by prefixed with +/- to reflect ascending/descending. Valid attributes: rating, like_count and play_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_song",
      "description": "Get details of a specific song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_privates",
      "description": "Show information about the song that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_song",
      "description": "Like a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_song",
      "description": "Unlike a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_songs",
      "description": "Get a list of songs you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked songs by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at, play_count and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_albums",
      "description": "Search for albums with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "min_release_date": {
            "type": "string",
            "description": "The minimum release date for search results in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_release_date": {
            "type": "string",
            "description": "The maximum release date for search results in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the albums by."
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the albums by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and release_date. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_album",
      "description": "Get details of a specific album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_privates",
      "description": "Show information about the album that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_album",
      "description": "Like a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_album",
      "description": "Unlike a album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_albums",
      "description": "Get a list of albums you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked albums by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_library",
      "description": "Get a list of playlists in the user's playlist library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether to show public playlists or private playlists."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_playlists",
      "description": "Search for playlists with a query. It will search over all public playlists and your own private playlists.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum like count for search results.",
            "default": 0
          },
          "max_like_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum like count for search results.",
            "default": 9223372036854775807
          },
          "min_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The minimum rating for search results.",
            "default": 0
          },
          "max_rating": {
            "type": "number",
            "maximum": 5.0,
            "minimum": 0.0,
            "description": "The maximum rating for search results.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: like_count, rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -like_count."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__create_playlist",
      "description": "Create a new playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "description": "The title of the playlist."
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether the playlist is public or not.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist",
      "description": "Get detailed information about a specific playlist. You can view your own playlists or others' playlists if they are public.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__delete_playlist",
      "description": "Delete a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to delete."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_playlist",
      "description": "Update a playlist title or privacy.",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "description": "The updated title of the playlist."
          },
          "is_public": {
            "type": "boolean",
            "description": "Whether the playlist is public or not."
          },
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to update."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_privates",
      "description": "Show information about the playlist that is private to the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__like_playlist",
      "description": "Like a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to like."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unlike_playlist",
      "description": "Unlike a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to unlike."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_liked_playlists",
      "description": "Get a list of playlists you have liked.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the liked playlists by prefixed with +/- to reflect ascending/descending. Valid attributes: liked_at and title.",
            "default": "-liked_at"
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__search_artists",
      "description": "Search for artists with a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "genre": {
            "type": "string",
            "description": "The genre to filter the artists by."
          },
          "min_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The minimum number of followers for search results.",
            "default": 0
          },
          "max_follower_count": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The maximum number of followers for search results.",
            "default": 9223372036854775807
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the artists by prefixed with +/- to reflect ascending/descending. Valid attributes: follower_count. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist",
      "description": "Get details of a specific artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__show_artist_following",
      "description": "Show if the user is following the artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_library",
      "description": "Get a list of songs in the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_song_to_library",
      "description": "Add a song to the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to add."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_song_from_library",
      "description": "Remove a song from the user's song library.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to remove."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_library",
      "description": "Get a list of albums in the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_album_to_library",
      "description": "Add an album to the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to add."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_album_from_library",
      "description": "Remove an album from the user's album library.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to remove."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_song_to_playlist",
      "description": "Add a song to a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to add the song to."
          },
          "song_id": {
            "type": "integer",
            "description": "The song id to add."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_song_from_playlist",
      "description": "Remove a song from a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to remove the song from."
          },
          "song_id": {
            "type": "integer",
            "description": "The song id to remove."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_downloaded_songs",
      "description": "Get a list of downloaded songs.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "min_downloaded_at": {
            "type": "string",
            "description": "Filter songs by minimum downloaded_at date in YYYY-MM-DD format.",
            "default": "1500-01-01"
          },
          "max_downloaded_at": {
            "type": "string",
            "description": "Filter songs by maximum downloaded_at date in YYYY-MM-DD format.",
            "default": "3000-01-01"
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the downloaded songs by prefixed with +/- to reflect ascending/descending. Valid attributes: created_at and downloaded_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page. If both query and sort_by are not given, null, or empty, sort_by will default to -downloaded_at."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_song",
      "description": "Download a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to download."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_downloaded_song",
      "description": "Remove a song from downloads.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to remove from downloads."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_following_artists",
      "description": "Get a list of artists the user is following.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__follow_artist",
      "description": "Follow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to follow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__unfollow_artist",
      "description": "Unfollow an artist.",
      "parameters": {
        "type": "object",
        "properties": {
          "artist_id": {
            "type": "integer",
            "description": "The artist id to unfollow."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_reviews",
      "description": "Get a list of reviews for a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "The song id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the song reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_song",
      "description": "Rate or review a song.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "song_id": {
            "type": "integer",
            "description": "ID of the song to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_review",
      "description": "Show a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__delete_song_review",
      "description": "Delete a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "ID of the song review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_song_review",
      "description": "Update a song review.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Song rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review."
          },
          "text": {
            "type": "string",
            "description": "Text content of the review."
          },
          "review_id": {
            "type": "integer",
            "description": "ID of the song review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_reviews",
      "description": "Get a list of reviews for an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "album_id": {
            "type": "integer",
            "description": "The album id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the album reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          }
        }
      }
    },
    {
      "name": "spotify__review_album",
      "description": "Rate or review an album.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_album_review",
      "description": "Show an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The album review id to retrieve."
          }
        }
      }
    },
    {
      "name": "spotify__delete_album_review",
      "description": "Delete an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "ID of the album review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_album_review",
      "description": "Update an album review.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Album rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review."
          },
          "text": {
            "type": "string",
            "description": "Text content of the review."
          },
          "review_id": {
            "type": "integer",
            "description": "ID of the album review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_reviews",
      "description": "Show a list of reviews for your playlist or others' public playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "playlist_id": {
            "type": "integer",
            "description": "The playlist id to retrieve reviews for."
          },
          "query": {
            "type": "string",
            "description": "The search query string.",
            "default": ""
          },
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "Email of the user to filter reviews by."
          },
          "min_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The minimum rating for a review.",
            "default": 1
          },
          "max_rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "The maximum rating for a review.",
            "default": 5
          },
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "sort_by": {
            "type": "string",
            "description": "The attribute to sort the playlist reviews by prefixed with +/- to reflect ascending/descending. Valid attributes: rating and created_at. If both query and sort_by are given and non-empty, results will be first ranked by query relevance, then paginated, and will then be sorted by the given attribute within each page."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__review_playlist",
      "description": "Rate or review a playlist.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review.",
            "default": ""
          },
          "text": {
            "type": "string",
            "description": "Text content of the review.",
            "default": ""
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_playlist_review",
      "description": "Show a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "The song review id to retrieve."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__delete_playlist_review",
      "description": "Delete a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "review_id": {
            "type": "integer",
            "description": "ID of the playlist review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_playlist_review",
      "description": "Update a playlist review.",
      "parameters": {
        "type": "object",
        "properties": {
          "rating": {
            "type": "integer",
            "maximum": 5.0,
            "minimum": 1.0,
            "description": "Playlist rating for this review."
          },
          "title": {
            "type": "string",
            "description": "Title of the review."
          },
          "text": {
            "type": "string",
            "description": "Text content of the review."
          },
          "review_id": {
            "type": "integer",
            "description": "ID of the playlist review."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_cards",
      "description": "Get a list of users payment cards.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_payment_card",
      "description": "Add a new payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "card_name": {
            "type": "string",
            "minLength": 1,
            "description": "Name of the payment card."
          },
          "owner_name": {
            "type": "string",
            "minLength": 1,
            "description": "Full name of the owner of the payment card."
          },
          "card_number": {
            "type": "integer",
            "exclusiveMaximum": 1e+16,
            "minimum": 1000000000000000.0,
            "description": "16-digit card number."
          },
          "expiry_year": {
            "type": "integer",
            "description": "Expiration year of the payment card."
          },
          "expiry_month": {
            "type": "integer",
            "maximum": 12.0,
            "minimum": 1.0,
            "description": "Expiration month of the payment card."
          },
          "cvv_number": {
            "type": "integer",
            "exclusiveMaximum": 1000.0,
            "minimum": 100.0,
            "description": "A 3-digit CVV number of the payment card."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_payment_card",
      "description": "Get details of a payment card.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be shown."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__delete_payment_card",
      "description": "Delete payment card information.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to be deleted."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__update_payment_card",
      "description": "Update payment card information.",
      "parameters": {
        "type": "object",
        "properties": {
          "card_name": {
            "type": "string",
            "minLength": 1,
            "description": "Name of the payment card to update."
          },
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to update."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_current_song",
      "description": "Show details of the current song on the queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__play_music",
      "description": "Play music based on various criteria. You can pass, at most, any one of queue_position, song_id, album_id or playlist_id. If one of song_id, album_id or playlist_id is passed, that song, album or playlist will be added to the queue and played. Otherwise, the queue will remain unchanged. If queue_position is passed, the song at that position in the queue will be played. If none is passed, the current song in the queue will be played.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to play."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to play."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to play."
          },
          "queue_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "Position of the song in the queue to play."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__pause_music",
      "description": "Pause the currently playing song.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__previous_song",
      "description": "Go to the previous song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__next_song",
      "description": "Go to the next song in the song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__move_song_in_queue",
      "description": "Move a song in the queue to a new position.",
      "parameters": {
        "type": "object",
        "properties": {
          "current_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The current position of the song in the queue."
          },
          "new_position": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The new position of the song in the queue."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__seek_song",
      "description": "Seek the current song to the given number of seconds.",
      "parameters": {
        "type": "object",
        "properties": {
          "seek_seconds": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The number of seconds to seek."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__loop_song",
      "description": "Set whether to loop the current song.",
      "parameters": {
        "type": "object",
        "properties": {
          "loop": {
            "type": "boolean",
            "description": "Whether to loop the current song."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__shuffle_song_queue",
      "description": "Shuffle songs in the music player queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_song_queue",
      "description": "Get the music player song queue. Songs are played in the order of the queue in a cycle.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__add_to_queue",
      "description": "Add a song, album or playlist to the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "song_id": {
            "type": "integer",
            "description": "ID of the song to add to queue."
          },
          "album_id": {
            "type": "integer",
            "description": "ID of the album to add to queue."
          },
          "playlist_id": {
            "type": "integer",
            "description": "ID of the playlist to add to queue."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__clear_song_queue",
      "description": "Clear the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__remove_song_from_queue",
      "description": "Remove a song at the given position from the music player song queue.",
      "parameters": {
        "type": "object",
        "properties": {
          "position": {
            "type": "integer",
            "description": "The 0-indexed position of the song in the queue."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_volume",
      "description": "Get the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__set_volume",
      "description": "Set the volume level of the music player.",
      "parameters": {
        "type": "object",
        "properties": {
          "volume": {
            "type": "integer",
            "maximum": 10.0,
            "minimum": 0.0,
            "description": "Volume level to set."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_recommendations",
      "description": "Get personalized song recommendations for the user.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__show_premium_plans",
      "description": "Show information about premium plans available.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "spotify__show_premium_subscriptions",
      "description": "Show your premium subscription history.",
      "parameters": {
        "type": "object",
        "properties": {
          "page_index": {
            "type": "integer",
            "minimum": 0.0,
            "description": "The index of the page to return.",
            "default": 0
          },
          "page_limit": {
            "type": "integer",
            "maximum": 20.0,
            "minimum": 1.0,
            "description": "The maximum number of results to return per page.",
            "default": 5
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__subscribe_premium",
      "description": "Subscribe to premium membership.",
      "parameters": {
        "type": "object",
        "properties": {
          "payment_card_id": {
            "type": "integer",
            "description": "ID of the payment card to use for buy premium subscription."
          },
          "duration": {
            "type": "string",
            "enum": [
              "monthly",
              "yearly"
            ],
            "description": "Duration of the premium subscription."
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    },
    {
      "name": "spotify__download_premium_subscription_receipt",
      "description": "Download the receipt for a premium subscription.",
      "parameters": {
        "type": "object",
        "properties": {
          "premium_subscription_id": {
            "type": "integer",
            "description": "ID of the premium subscription to download the receipt for."
          },
          "file_system_access_token": {
            "type": "string",
            "description": "Access token obtained from file_system app login."
          },
          "download_to_file_path": {
            "type": "string",
            "description": "The file path to download the receipt file to in file system app. Path can be absolute, starting with '/', or relative to the user's home directory, starting with '~/'. If not passed, it will be saved in your ~/downloads directory."
          },
          "overwrite": {
            "type": "boolean",
            "description": "Whether to overwrite the file if it already exists.",
            "default": false
          },
          "access_token": {
            "type": "string",
            "description": "Access token obtained from spotify app login."
          }
        }
      }
    }
  ]
}

## Communication Steps

### Step 1 · outer 0 · dispatch 3 · round 0

- Phase: se_g_transaction_plan
- Parallel: False
- Shared Prompt IDs: p_1, p_2, p_3, p_4

#### agent_0 (coordinator)
- Unique Prompt IDs: _None_
- Inbox Message IDs: _None_
- Tool Calls: _None_

```text
{"answer_artifact":{"plan":"1) Authenticate to Spotify using supervisor credentials (supervisor__show_account_passwords -> spotify__login) to obtain access_token. 2) Enumerate the user's album library via spotify__show_album_library (paginate with page_limit=20 until exhausted) to get the full set of album IDs. 3) For each album, retrieve its tracks (spotify__show_album / spotify__search_songs filtered by album_id) and determine each song's play count (spotify__show_song_privates or search_songs play_count field) to identify the single most-played song per album. 4) Assemble the ordered list of winning song IDs (one per album). 5) Create the playlist 'My Most Played Album Songs' and add the selected songs. NOTE: playlist creation/add-song tools are not present in this stage's toolset; the committer must use the appropriate playlist-creation API (verify via api_docs__show_api_descriptions('spotify')).","task_package":{"committer_steps":["Login and capture access_token","Paginate show_album_library to collect all album IDs","For each album, list songs and compare play_count; select max (tie-break: highest play_count, then lowest song_id)","Create playlist titled exactly 'My Most Played Album Songs'","Add the selected song IDs to the playlist"],"preconditions_to_verify":["Album library is non-empty","Each album has at least one song with a play_count","Playlist with this exact name does not already exist (check show_playlist_library)"],"proposed_mutation":"Create playlist 'My Most Played Album Songs' and populate with one most-played song per album in the album library"},"open_questions":["Playlist creation/add-song API names not confirmed in this stage's toolset; must be verified via api_docs before committing","Whether 'most played' uses user-specific play_count (private) vs global play_count"]},"summary":"Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.","critique":"No tool outputs were retrieved in this stage, so album IDs, song IDs, and play counts are unknown. The playlist-creation API is not in the available toolset, so the exact mutation call cannot yet be specified with canonical arguments.","revision_request":"Next stage should execute the read-only enumeration (login, album library pagination, per-album song play counts) and confirm the playlist-creation API signature via api_docs before the committer performs the mutation.","confidence":0.25,"unresolved_issues":["Album library contents unknown","Per-album most-played songs unknown","Playlist creation/add-song API not confirmed","Definition of 'most played' (user vs global) unverified"],"evidence_summary":"No tool calls were executed in this planning stage; the plan is based solely on the task instruction and the available tool list. No album, song, or play-count data has been retrieved."}
```

#### Messages Sent

- m_1: agent_0 -> agent_1 [task_package]
  Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.
- m_2: agent_0 -> agent_2 [task_package]
  Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet.

#### Termination

_None_

### Step 2 · outer 0 · dispatch 4 · round 0

- Phase: se_g_transaction_work
- Parallel: True
- Shared Prompt IDs: p_2, p_3

#### agent_1 (worker)
- Unique Prompt IDs: p_5, p_6
- Inbox Message IDs: m_1
- Tool Calls: supervisor__show_account_passwords (completed), api_docs__show_api_descriptions (completed), spotify__login (completed), api_docs__show_api_doc (completed), api_docs__show_api_doc (completed), supervisor__show_profile (completed), spotify__login (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed)

```text
I need the correct email. Let me check the profile.
```

#### agent_2 (worker)
- Unique Prompt IDs: p_7, p_8
- Inbox Message IDs: m_2
- Tool Calls: supervisor__show_account_passwords (completed), api_docs__show_api_descriptions (completed), supervisor__show_profile (completed), api_docs__show_api_doc (completed), api_docs__show_api_doc (completed), spotify__login (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed)

```text
I need the email for login. Let me check the profile and log in.
```

#### Messages Sent

- m_3: agent_1 -> agent_0 [specialist_report]
  I need the correct email. Let me check the profile.
- m_4: agent_2 -> agent_0 [specialist_report]
  I need the email for login. Let me check the profile and log in.

#### Termination

_None_

### Step 3 · outer 0 · dispatch 5 · round 0

- Phase: se_g_transaction_merge
- Parallel: False
- Shared Prompt IDs: p_2, p_3, p_9, p_10

#### agent_0 (coordinator)
- Unique Prompt IDs: _None_
- Inbox Message IDs: digest_agent_0_r0_3, m_3, m_4
- Tool Calls: supervisor__show_profile (completed), supervisor__show_account_passwords (completed), spotify__login (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed)

```text
I'll start by getting the supervisor's credentials and profile to log in.
```

#### Messages Sent

- digest_agent_0_r0_3: shared_context -> agent_0 [evidence_digest]
  Evidence ledger (scope=global, 3 entries): agent_0[r0]: Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet. | evidence: No tool calls were executed in this planning stage; the plan is based solely on the task instruction and the available tool list. No album; song; or play-count data has been retrieved. || agent_1[r0]: I need the correct email. Let me check the profile. || agent_2[r0]: I need the email for login. Let me check the profile and log in.

#### Termination

_None_

### Step 4 · outer 0 · dispatch 11 · round 1

- Phase: se_g_transaction_plan
- Parallel: False
- Shared Prompt IDs: p_1, p_2, p_3, p_11

#### agent_0 (coordinator)
- Unique Prompt IDs: _None_
- Inbox Message IDs: _None_
- Tool Calls: _None_

```text
{"answer_artifact":"Plan (read-only stage; no mutations performed):\n1. Auth: call supervisor__show_account_passwords to get Spotify credentials, then spotify__login to obtain access_token.\n2. Enumerate album library: spotify__show_album_library (paginate page_limit=20 until exhausted) to collect all album_ids in the user's album library.\n3. Per album: spotify__show_album(album_id) to get its song list; for each song use spotify__show_song_privates(song_id, access_token) to read the user's play_count; select the song with the highest play_count per album (tie-break: higher rating, then lower song_id).\n4. Precondition check: verify no existing playlist named 'My Most Played Album Songs' via spotify__show_playlist_library; if one exists, report and plan to reuse/update it rather than duplicate.\n5. Proposed mutation for committer: create playlist 'My Most Played Album Songs' and add exactly one song_id per album (the per-album max-play song). Note: no create-playlist/add-song API is exposed in the visible toolset, so the committer must confirm the correct mutation API (likely via api_docs__show_api_descriptions('spotify')) before executing.\n6. Verify post-mutation by reading the playlist back and confirming one song per album.","summary":"Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.","critique":"Prior artifact only stated intent to log in; it did not enumerate albums, compute per-album most-played songs, or identify the playlist-creation API. Also, the visible toolset lacks an explicit create-playlist/add-song tool, which must be resolved before committing.","revision_request":"Committer should first confirm the playlist creation/population API via api_docs, then execute the single create-and-populate mutation with canonical album/song IDs derived from the album library and private play counts.","confidence":0.25,"unresolved_issues":["No explicit create-playlist or add-song-to-playlist tool visible; must confirm via API docs.","Album library contents and per-song play counts not yet retrieved.","Whether a playlist with the target name already exists is unknown."],"evidence_summary":"No tool outputs retrieved yet in this stage; plan is based solely on the task instruction and the visible tool list (spotify__show_album_library, spotify__show_album, spotify__show_song_privates, spotify__show_playlist_library, supervisor__show_account_passwords)."}
```

#### Messages Sent

- m_5: agent_0 -> agent_1 [orchestrator_feedback]
  Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.
- m_6: agent_0 -> agent_2 [orchestrator_feedback]
  Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.
- m_7: agent_0 -> agent_3 [orchestrator_feedback]
  Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage.

#### Termination

_None_

### Step 5 · outer 0 · dispatch 12 · round 1

- Phase: se_g_transaction_work
- Parallel: True
- Shared Prompt IDs: p_2, p_3

#### agent_1 (worker)
- Unique Prompt IDs: p_5, p_12
- Inbox Message IDs: m_5
- Tool Calls: supervisor__show_active_task (completed), supervisor__show_account_passwords (completed), api_docs__show_api_descriptions (completed), supervisor__show_profile (completed), api_docs__show_api_doc (completed), api_docs__show_api_doc (completed), spotify__login (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed)

```text
I need the email for login. Let me check the profile and log in.
```

#### agent_2 (worker)
- Unique Prompt IDs: p_7, p_13
- Inbox Message IDs: m_6
- Tool Calls: supervisor__show_active_task (completed), supervisor__show_account_passwords (completed), supervisor__show_profile (completed), spotify__login (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed)

```text
I'll start by gathering the account credentials and checking the active task.
```

#### agent_3 (worker)
- Unique Prompt IDs: p_14, p_15
- Inbox Message IDs: m_7
- Tool Calls: supervisor__show_active_task (completed), supervisor__show_account_passwords (completed), supervisor__show_profile (completed), api_docs__show_api_descriptions (completed), spotify__login (completed), api_docs__show_api_doc (completed), api_docs__show_api_doc (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_album (completed), spotify__show_album (completed), spotify__show_album_privates (completed), spotify__search_songs (completed), spotify__search_songs (completed), spotify__search_songs (completed), spotify__search_songs (completed)

```text
I'll start by verifying the task and gathering the needed evidence.
```

#### Messages Sent

- m_10: agent_3 -> agent_0 [specialist_report]
  I'll start by verifying the task and gathering the needed evidence.
- m_8: agent_1 -> agent_0 [specialist_report]
  I need the email for login. Let me check the profile and log in.
- m_9: agent_2 -> agent_0 [specialist_report]
  I'll start by gathering the account credentials and checking the active task.

#### Termination

_None_

### Step 6 · outer 0 · dispatch 13 · round 1

- Phase: se_g_transaction_merge
- Parallel: False
- Shared Prompt IDs: p_2, p_3, p_9, p_16

#### agent_0 (coordinator)
- Unique Prompt IDs: _None_
- Inbox Message IDs: digest_agent_0_r1_8, m_8, m_9, m_10
- Tool Calls: supervisor__show_active_task (completed), supervisor__show_account_passwords (completed), supervisor__show_profile (completed), spotify__login (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_playlist_library (completed), spotify__show_album_library (completed), spotify__show_album (completed), spotify__show_album (completed), spotify__search_songs (completed), spotify__search_songs (completed)

```text
I'll start by gathering credentials and the active task.
```

#### Messages Sent

- digest_agent_0_r1_8: shared_context -> agent_0 [evidence_digest]
  Evidence ledger (scope=global, 8 entries): agent_0[r0]: Read-only planning stage. Produced a bounded plan to enumerate the album library, compute the most-played song per album, and create/populate the playlist 'My Most Played Album Songs'. No mutations performed; no data retrieved yet. | evidence: No tool calls were executed in this planning stage; the plan is based solely on the task instruction and the available tool list. No album; song; or play-count data has been retrieved. || agent_1[r0]: I need the correct email. Let me check the profile. || agent_2[r0]: I need the email for login. Let me check the profile and log in. || agent_0[r0]: I'll start by getting the supervisor's credentials and profile to log in. || agent_0[r1]: Bounded plan: authenticate, enumerate album library, compute per-album most-played song via private play counts, check for existing playlist, then hand off a single create-and-populate mutation to the committer. No mutation executed in this read-only stage. | evidence: No tool outputs retrieved yet in this stage; plan is based solely on the task instruction and the visible tool list (spotify__show_album_library; spotify__show_album; spotify__show_song_privates; spotify__show_playlist_library; supervisor__show_account_passwords). || agent_1[r1]: I need the email for login. Let me check the profile and log in. || agent_2[r1]: I'll start by gathering the account credentials and checking the active task. || agent_3[r1]: I'll start by verifying the task and gathering the needed evidence.

#### Termination

_None_
