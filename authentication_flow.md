# Auth flow
1. Create new user
   * `POST /auth`
     * Request:
       * Body:
         ```
         {
            "emails": string[],
            "password": {
                 "new": string,
                 "repeat": string
            }
         }
         ```
     * Response: 
       * status: 204 No content
     * Side effects:
       * Create the user in user table
       * for every email in the body create an entry in email and in verification table
       * Send email to every address given in the body containing its verification id
2. Verify the email
   * `GET /auth/:verification`
     * Request:
       * Headers:
         * Authorization: Basic auth with verifying email and password
     * Response:
       * status:
         * 201 created: successful request
         * 400 bad: this verification no longer exists or never existed. 
       * Body:
         ```
         some.example.jwt
         ```
     * Side effects:
       * verification is marked as completed in verification table
       * a session in session table is created. The sessions refresh token is sent in the JWT. This refresh token \
         is only sent when user first is verified with `GET /auth/:verification` and when user authenticates with \ 
         `GET /auth` otherwise this refresh token is not set in the JWT
3. Sign in
   * `GET /auth`
     * Request:
       * Headers:
         * Authorization:
           * Basic auth with a verified email + password
     * Response:
       * status: 200 
       * Body:
         ```
         some.example.jwt
         ```
     * Side effects:
       * new session is added / updated in the session table
       * the user is notified by email if a new row in the session table was created. \ 
         If it is the same host / useragent the row is only updated with the new refresh_token
4. Refresh JWT
   * `GET /auth/refresh`
     * Request:
       * Headers:
         * Authorization:
           * Basic auth with userid / email + refresh token
     * Response:
       * status: 200
       * Body:
         ```
         some.example.jwt
         ```