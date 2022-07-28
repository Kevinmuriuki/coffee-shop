/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-3qhgi85p.us', // the auth0 domain prefix
    audience: 'https://127.0.0.1:5000', // the audience set for the auth0 app
    clientId: 'iqVNEV4d3aXlqKRVTSNQ2va2HSs9tKNJ', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:4200', // the base url of the running ionic application. 
  }
};
