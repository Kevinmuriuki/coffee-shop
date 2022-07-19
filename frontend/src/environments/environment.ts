/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-3qhgi85p.us.auth0.com', // the auth0 domain prefix
    audience: 'coffee shop', // the audience set for the auth0 app
    clientId: 'FX8o40YgtYsLEa80cONv8WuYL1twGyrK', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application. 
  }
};
