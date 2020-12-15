/* @TO_DO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  // the running FLASK api server url
  apiServerUrl: 'http://127.0.0.1:5000',
  auth0: {
    // the auth0 domain prefix
    url: 'dev-mv6js4zd.us',
    // the audience set for the auth0 app
    audience: 'CoffeShopDrinks',
    // the client id generated for the auth0 app
    clientId: '7XFuubVgUFVzNcYMNU9gWOxz4j6Qd3WQ',
    // the base url of the running ionic application.
    callbackURL: 'http://localhost:8100'
  }
};
