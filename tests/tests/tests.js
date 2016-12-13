var waitTimeout = 1000; // milliseconds

var extended = function(browser) {
  browser.clickOn = function(text) {
    return this
      .useXpath()
      .click('//*[contains(text(), "'+text+'")]')
      .useCss();
  };
  browser.selectRadioButton = function(text) {
    return this
      .useXpath()
      .click('//label[contains(span/text(), "'+text+'")]')
      .useCss()
  };
  return browser;
}

var login = function(browser, email, password) {
  extended(browser)
    .url(process.env.APP_SERVER_URL)
    .waitForElementVisible('body', waitTimeout)
    .assert.containsText('h1', 'Publish and update data')
    .clickOn('Sign in')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'Sign in')
    .setValue('input[name=email]', email)
    .setValue('input[name=password]', password)
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout);
  return browser;
}

// ============ here start the tests ===========================================

module.exports = {
  'Failed login' : function(browser) {
    login(browser, 'bad', 'bad')
    .assert.containsText('h1', 'There was a problem')
    .end()
  },

  'Create a dataset happy path' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .assert.containsText('h1', 'Dashboard')
    .clickOn('Create a dataset')
    .assert.containsText('h1', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'Choose an area')
    .selectRadioButton('England')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'How often is this dataset updated?')
    .end();
  },

  'Create a dataset missing title' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .assert.containsText('h1', 'Dashboard')
    .clickOn('Create a dataset')
    .assert.containsText('h1', 'Create a dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1.error-summary-heading', 'There was a problem')
    .assert.containsText('ul.error-summary-list', 'Please provide a valid title')
    .end();
  },

  'Create a dataset, invalid title' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .assert.containsText('h1', 'Dashboard')
    .clickOn('Create a dataset')
    .assert.containsText('h1', 'Create a dataset')
    .setValue('input[name=title]', '][;')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1.error-summary-heading', 'There was a problem')
    .assert.containsText('ul.error-summary-list', 'Please provide a valid title')
    .end();
  },

  'Create a dataset missing description' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .assert.containsText('h1', 'Dashboard')
    .clickOn('Create a dataset')
    .assert.containsText('h1', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1.error-summary-heading', 'There was a problem')
    .assert.containsText('ul.error-summary-list', 'Please provide a description')
    .end();
  },

  'Create a dataset, omit the licence' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickOn('Create a dataset')
    .waitForElementVisible('main', waitTimeout)
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1.error-summary-heading', 'There was a problem')
    .assert.containsText(
      'ul.error-summary-list',
      'Please select a licence for your dataset'
    )
    .end();
  },

  'Create a dataset, other licence, leave input empty' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickOn('Create a dataset')
    .waitForElementVisible('main', waitTimeout)
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .clickOn('Other:')
    .submitForm('form')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1.error-summary-heading', 'There was a problem')
    .assert.containsText(
      'ul.error-summary-list',
      'Please type the name of your licence'
    )
    .end();
  }
};
