var waitTimeout = 1000; // milliseconds

var extended = function(browser) {
  browser.clickOn = function(element, text) {
    return this
      .useXpath()
      .click('//' + element + '[contains(text(), "'+text+'")]')
      .useCss();
  };
  browser.clickOnLink = function(text) {
    return this.clickOn('a', text);
  };
  browser.clickOnButton = function(text) {
    return this.clickOn('button', text);
  };
  browser.selectRadioButton = function(text) {
    return this
      .useXpath()
      .click('//label[contains(span/text(), "'+text+'")]')
      .useCss();
  };
  browser.submitFormAndCheckNextTitle = function(title) {
    return this
      .submitForm('form')
      .waitForElementVisible('h1', waitTimeout)
      .assert.containsText('h1', title);
  };
  browser.clickAndCheckNextTitle = function(linkText, title) {
    return this
      .clickOnLink(linkText)
      .waitForElementVisible('h1', waitTimeout)
      .assert.containsText('h1', title);
  };
  browser.checkError = function(text) {
    return this
      .assert.containsText('ul.error-summary-list', text);
  };

  browser.checkFormInput = function(name) {
    return this
      .assert.elementPresent('input[name=' + name + ']');
  };

  return browser;
}

var login = function(browser, email, password) {
  extended(browser)
    .url(process.env.APP_SERVER_URL)
    .waitForElementVisible('body', waitTimeout)
    .assert.containsText('h1', 'Publish and update data')
    .clickOnLink('Sign in')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'Sign in')
    .setValue('input[name=email]', email)
    .setValue('input[name=password]', password)
    .submitFormAndCheckNextTitle('Dashboard');
  return browser;
}

// ============ here start the tests ===========================================

module.exports = {
  'Failed login' : function(browser) {
    extended(browser)
    .url(process.env.APP_SERVER_URL)
    .waitForElementVisible('body', waitTimeout)
    .assert.containsText('h1', 'Publish and update data')
    .clickOnLink('Sign in')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'Sign in')
    .setValue('input[name=email]', 'foo@bar.baz')
    .setValue('input[name=password]', 'qux')
    .submitFormAndCheckNextTitle('There was a problem signing you in')
    .end()
  },

  'Create a dataset, happy path' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every month')
    .submitFormAndCheckNextTitle('Add a link')
    .setValue('input[name=addfile_monthly-url]', 'http://example.com/data.csv')
    .setValue('input[name=addfile_monthly-title]', 'Title of this link')
    .setValue('input[name=period_month]', '12')
    .setValue('input[name=period_year]', '2016')
    .submitFormAndCheckNextTitle('Dataset links')
    .submitFormAndCheckNextTitle('Get notifications')
    .selectRadioButton('Yes')
    .submitFormAndCheckNextTitle('Check your dataset')
//    .submitFormAndCheckNextTitle('Your dataset has been published')
    .end();
  },

  'Create a dataset, missing title' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a valid title')
    .setValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
  },

  'Create a dataset, invalid title' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', '][;')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a valid title')
    .setValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
  },

  'Create a dataset missing description' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a description')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
  },

  'Create a dataset missing summary' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a summary')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
  },

  'Create a dataset, omit the organisation' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please choose which organisation will own this dataset')
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .end();
  },

  'Create a dataset, omit the licence' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please select a licence for your dataset')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .end();
  },

  'Create a dataset, other licence, leave input empty' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Other:')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please type the name of your licence')
    .setValue('input[name=licence-licence_other]', 'other licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .end();
  },

  'Create a dataset, no region chosen' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please select the area that your dataset covers')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .end();
  },

  'Create a dataset, no frequency chosen' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please indicate how often this dataset is updated')
    .selectRadioButton('Every day')
    .submitFormAndCheckNextTitle('Add a link')
    .end();
  },

  'Create a dataset, frequency daily' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every day')
    .submitFormAndCheckNextTitle('Add a link')
    .end();
  },

  'Create a dataset, frequency weekly' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every week')
    .submitFormAndCheckNextTitle('Add a link')
    .checkFormInput('addfile_weekly-start_day')
    .checkFormInput('addfile_weekly-end_day')
    .end();
  },

  'Create a dataset, frequency monthly' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every month')
    .submitFormAndCheckNextTitle('Add a link')
    .checkFormInput('period_month')
    .checkFormInput('period_year')
    .end();
  },

  'Create a dataset, frequency quarterly' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every quarter')
    .submitFormAndCheckNextTitle('Add a link')
    .checkFormInput('period_quarter')
    .end();
  },

  'Create a dataset, frequency yearly' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .setValue('input[name=title]', 'Title of my dataset')
    .setValue('textarea[name=summary]', 'Summary of my dataset')
    .setValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every year (January to December)')
    .submitFormAndCheckNextTitle('Add a link')
    .checkFormInput('period_year')
    .end();
  },

  'Dashboard' : function (browser) {
    login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .assert.containsText('main', 'Update datasets')
    .assert.containsText('main', 'Fix datasets')
    .end()
  }


};
