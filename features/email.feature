Feature: As an email client user I can attach an image in an email so that I can send it to a recipient
  # Normal Flow
  Scenario: Sending email with attached image from local computer and specified recipient
    Given I am a user with a valid outlook email address
    And I am logged in to my email
    When I press “new message”
    And I enter a recipient in the “To” input field
    And I enter a subject
    And I add an image to the e-mail body
    And I press “Send”
    Then the email should send to the specified recipient 

  # Alternate Flow
  Scenario: Replying to an email with an attached image
    Given I am a user with a valid outlook email address
    And I am logged in to my email
    And I have an e-mail to reply to
    When I reply to the e-mail
    And I enter another recipient in the reply
    And I add an image to the e-mail body
    And I press “Send”
    Then the email should send to the specified recipient 

  # Error Flow
  Scenario: Sending email with unspecified recipient
    Given I am a user with a valid outlook email address
    And I am logged in to my email
    When I press “new message”
    And I enter a subject
    And I do not specify a recipient
    And I add an image to the e-mail body
    And I press “Send”
    Then an error message displays prompting me to enter at least one recipient
