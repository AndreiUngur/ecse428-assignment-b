Feature: As an email client user I can attach an image in an email so that I can send it to a recipient

  # Background
  Background: some requirement of this test
    Given I am a user with a valid outlook email address
    And I am logged in to my email


  # Normal Flow
 Scenario Outline: Sending email with attached image from local computer and specified recipient
   Given I want to send a new message to <address>
   When the subject to my e-mail is: A friendly bug.
   And the image <attachment> is attached in the e-mail body
   And I send my e-mail
   Then an email with <attachment> attached for <address> should appear in my Sent folder

 Examples: E-mail contents
   | address                     | attachment          |
   | andrei.ungur@mail.mcgill.ca | friendlybug.gif     |
   | andreiskate2@hotmail.com    | friendlybug.gif     |
   | andrei.u96@hotmail.com      | solaire.png         |
   | andreiskate@hotmail.com     | background.jpeg     |
   | random856394@mailinator.com | biggerimage.jpg     |


  # Alternate Flow
  Scenario Outline: Replying to an email with an attached image
    Given I have an e-mail to reply to
    When I reply to the e-mail
    And I include <address> in the reply
    And the image <attachment> is attached in the e-mail body
    And I send my e-mail
    Then an email with <attachment> attached for <address> should appear in my Sent folder

  Examples: E-mail contents
    | address                     | attachment          |
    | andrei.ungur@mail.mcgill.ca | friendlybug.gif     |
    | andreiskate2@hotmail.com    | friendlybug.gif     |
    | andrei.u96@hotmail.com      | solaire.png         |
    | andreiskate@hotmail.com     | background.jpeg     |
    | random856394@mailinator.com | biggerimage.jpg     |


  # Error Flow
  Scenario Outline: Sending email with unspecified recipient
    Given I want to send a new message
    When I do not have a recipient
    And the subject to my e-mail is: A friendly bug.
    And the image <attachment> is attached in the e-mail body
    And I send my e-mail
    Then the system warns me to enter at least one recipient

  Examples: E-mail contents
    | attachment        |
    | friendlybug.gif   |
    | solaire.png       |
    | background.jpeg   |
    | bigimage.jpg      |
    | biggerimage.jpg   |
