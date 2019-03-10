from behave import *
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import time

# Get the variables the user must set for the test to run.
# Warn the user if these are not set as the test can not run.
username = os.environ.get("email_username", "")
password = os.environ.get("email_password", "")


error_message_ref = "//span[contains(text(),'This message must have at least one recipient.')]"
email_subject = "A friendly bug."
reply_email_subject = "Send me bugs."
timeout_seconds = 8
short_timeout = 3
long_timeout = 15
browser = webdriver.Chrome()


@given('I am a user with a valid outlook email address')
def step_impl(context):
    """
    Background step, preliminary even to logging in
    """
    assert username and password


@given('I am logged in to my email')
def step_impl(context):
    """
    Sets up the user's testing environment by logging in

    The flow first assumes the user is completely logged out
    and attemps to log in.

    If it fails, we assume the user is already logged in.

    Modifications made by Outlook to their log-in flow would need
    to be reflected here.
    """
    goto_inbox()

    # Try to log in
    try:
        # Send username
        email_element = browser.find_element_by_name('loginfmt')
        email_element.send_keys(username)
        continue_button = browser.find_element_by_id('idSIButton9')
        continue_button.click()

        # Wait for the password input to appear
        WebDriverWait(browser, timeout_seconds).until( 
            expected_conditions.presence_of_element_located( 
                (By.ID, 'passwordInput')
            )
        )

        # Send password
        password_element = browser.find_element_by_id('passwordInput')
        password_element.send_keys(password)

        login_button = browser.find_element_by_id('submitButton')
        login_button.click()

        # Wait for the screen to ask if we want to save our login info
        WebDriverWait(browser, timeout_seconds).until( 
            expected_conditions.presence_of_element_located( 
                (By.ID, 'idBtn_Back')
            )
        )

        # Choose to not save log-in info
        dont_save_login_button = browser.find_element_by_id('idBtn_Back')
        dont_save_login_button.click()

        # Wait until we're successfully logged in
        WebDriverWait(browser, timeout_seconds).until( 
            expected_conditions.presence_of_element_located( 
                (By.XPATH, "//*[contains(text(),'Inbox')]")
            )
        )
    except NoSuchElementException:
        # If we couldn't find an element, it could be because we're already logged in.
        # If we see the "Inbox", we are already logged in.
        inbox_element = browser.find_element_by_xpath("//*[contains(text(),'Inbox')]")


@given('I have an e-mail to reply to')
def step_impl(context):
    """
    The user sends an e-mail to themselves to enable the possibility of replying.
    """
    create_new_email()

    # We track the email's subject as it is re-used later
    context.email_subject = reply_email_subject

    # Send e-mail to yourself then go back to inbox
    enter_subject(reply_email_subject)
    add_recipient(username)
    send_email()
    goto_inbox()

    # Wait for the e-mail we sent ourselves to be visible.
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//div[contains(@aria-label, '{reply_email_subject}')]")
        )
    )


@given('I want to send a new message to {address}')
def step_impl(context, address):
    """
    Regular scenario of sending an email to a recipient
    """

    # We track the email's subject as it is re-used later
    context.email_subject = email_subject

    # We ensure that the email isn't part of our "Sent" e-mails already
    goto_sent_items()
    sent_email_title = browser.find_elements_by_xpath(f"//*[contains(text(),'{email_subject}')]")
    assert not sent_email_title

    # Create new e-mail
    create_new_email()

    # Add recipient
    add_recipient(address)


@given('I want to send a new message')
def step_impl(context):
    """
    Error scenario of sending an email to no recipient
    """
    context.email_subject = email_subject

    # Create new e-mail
    create_new_email()


@when('I do not have a recipient')
def step_impl(context):
    """
    Also part of the error scenario, nothing happens here.
    """
    pass


@when('the subject to my e-mail is: A friendly bug.')
def step_impl(context):
    """
    Regular scenario, we add the subject here.
    """
    enter_subject(context.email_subject)


@when('the image {attachment} is attached in the e-mail body')
def step_impl(context, attachment):
    """
    Used across all scenarios to ensure it is possible to attach images.
    """
    attach_file(attachment)


@when('I reply to the e-mail')
def step_impl(context):
    """
    Alternate scenario to ensure it is possible to reply with an attachment
    """

    # Find the email we sent ourselves
    browser.find_element_by_xpath(f"//div[contains(@aria-label,'{context.email_subject}')]").click()

    # Wait for reply button to appear, click reply
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, "//div[contains(@aria-label, 'Content pane')]//button[@aria-label='Reply']")
        )
    )
    browser.find_element_by_xpath("//div[contains(@aria-label,'Content pane')]//button[@aria-label='Reply']").click()

    # Wait for "To:" field to appear, where we will add a new recipient, and click it.
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, "//label[contains(text(),'To:')]")
        )
    )
    browser.find_element_by_xpath("//label[contains(text(),'To:')]").click()


@when('I include {address} in the reply')
def step_impl(context, address):
    """
    Alternate scenario includes adding an additional recipient to the message
    """
    add_recipient(address)


@when('I send my e-mail')
def step_impl(context):
    """
    Used across all scenarios to send the email.
    
    When an email is sent, we first ensure that it was valid
    (i.e.: no error message appeared). If this is the case, we go back to the inbox.

    The refresh to "inbox" is because sometimes Outlook needs a refresh to see the new e-mail.
    """
    email_valid  = send_email()
    if email_valid:
        goto_inbox()


@then('an email with {attachment} attached for {address} should appear in my Sent folder')
def step_impl(context, attachment, address):
    """
    Validates regular and alternate scenarios by verifying that the correct e-mail is present
    in the Sent folder.

    If the e-mail subject and the attachment can be found in our Sent folder, we don't need
    to spend time also looking for the recipient as they are the only ones our e-mail was sent to.
    We ensure this by checking that no e-mail with the subject is found prior to the test, and
    including the recipient from the test in the "To:" input.

    The "To:" input is itself is further tested by our error flow.
    """
    goto_sent_items()

    # Generic references to DOM elements that are reused multiple times later
    email_card_ref = f"//div[contains(@aria-label, 'Has attachments {context.email_subject}')]"
    image_ref = f"//div[@aria-label='{attachment} Open']"

    # Ensure that the e-mail subject can be found in the Sent folder
    WebDriverWait(browser, long_timeout).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, email_card_ref)
        )
    )
    browser.find_element_by_xpath(email_card_ref).click()

    # Ensure that the attachment can be found in the Sent folder
    WebDriverWait(browser, long_timeout).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, image_ref)
        )
    )   
    attachment_element = browser.find_element_by_xpath(image_ref)
    assert attachment_element is not None

    # Delete e-mail to revert back to initial state
    remove_sent_email(context.email_subject)

    # Delete e-mail from the inbox if the test involved sending an e-mail to ouselves.
    cleanup_inbox(context.email_subject)


@then('the system warns me to enter at least one recipient')
def step_impl(context):
    """
    Error flow shows a error badge because a recipient is missing.
    """

    # Reference to DOM element is re-used later
    error_badge_ref = "//i[@data-icon-name='ErrorBadge']"
    WebDriverWait(browser, short_timeout).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, error_message_ref)
        )
    )
    error_badge = browser.find_element_by_xpath(error_badge_ref)
    error_message = browser.find_element_by_xpath(error_message_ref)
    assert error_badge and error_message

    # Discard email as it has served its purpose.
    browser.find_element_by_xpath("//button[@aria-label='Discard']").click()
    browser.find_element_by_id('ok-1').click()


"""
Helper functions:
Below are helper functions re-used across the various tests.
"""
def remove_sent_email(subject):
    """
    Removes an e-mail whose subject is `subject`.
    """

    # References to DOM elements re-used multiple times
    email_card_ref = f"//div[contains(@aria-label, 'Has attachments {subject}')]"
    delete_button_ref = f"//div[contains(@aria-label, 'Has attachments {subject}')]//button[@title='Delete']"

    # Locate e-mail
    WebDriverWait(browser, short_timeout).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, email_card_ref)
        )
    )
    email_card = browser.find_element_by_xpath(email_card_ref)

    # Delete sent email to restore initial conditions
    hoverover = ActionChains(browser).move_to_element(email_card).click().perform()
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, delete_button_ref)
        )
    )

    # Wait until the e-mail is invisible
    browser.find_element_by_xpath(delete_button_ref).click()
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.invisibility_of_element_located( 
            (By.XPATH, email_card_ref)
        )
    )


def cleanup_inbox(subject):
    """
    Similar to `remove_sent_email`, but ensures we are in the `inbox` folder first.

    Regular and Alternate scenarios go to the Sent folder, from which `remove_sent_email` is called.
    Sometimes we also have lingering emails in the inbox.
    """
    goto_inbox()
    try:
        remove_sent_email(subject)
    except (NoSuchElementException, TimeoutException):
        pass


def create_new_email():
    """
    Creates new e-mail (without specifying subject, recipient or body)
    """

    # Find button and click it (we go by class name as it's unique enough)
    new_mail_button = browser.find_element_by_class_name('_39t1Yy85WX6tG-kM3-jR-t')
    new_mail_button.click()

    # Wait until we see the new message form
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.CLASS_NAME, 'pickerInput_269bfa71')
        )
    )


def enter_subject(subject):
    """
    Enters a subject to the e-mail, assuming we have a new e-mail form
    """
    subject_element = browser.find_element_by_id('subjectLine0')
    subject_element.send_keys(subject)


def add_recipient(recipient):
    """
    Adds a recipient to the e-mail, assuming we have a new e-mail form
    """
    recipient_element = browser.find_element_by_class_name('pickerInput_269bfa71')
    recipient_element.send_keys(recipient)

    # Sometimes we are given suggestions of contacts with the e-mail we gave as input
    try:
        # Wait until we see the user suggestion picker
        WebDriverWait(browser, timeout_seconds).until( 
            expected_conditions.presence_of_element_located( 
                (By.ID, 'sug-0')
            )
        )

        suggestion_button = browser.find_element_by_id('sug-0')
        suggestion_button.click()
    except TimeoutException:
        # This just means we couldn't get a good suggestion by outlook
        # for this recipient. We can just send the e-mail regardless.
        pass


def attach_file(filename):
    """
    Attaches a file to the e-mail, assuming we have a new e-mail form.

    If the image is too large, it will also click on the prompt asking how we want
    to deal with the large file.
    """

    # Get full file path relative to script location
    file_to_send = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                filename)

    # Find input DOM element for files and send our file path to it
    body_element = browser.find_element_by_xpath("//input[@type='file' and @accept='*/*']")
    body_element.send_keys(file_to_send)

    # Define a (potentially) longer timeout for very big files (which take a while to upload, this is normal)
    longer_timeout = timeout_seconds

    try:
        # If the file is huge, a popup will appear. Click "Attach", else ignore it
        WebDriverWait(browser, 2).until( 
            expected_conditions.presence_of_element_located( 
                (By.XPATH, "//button[contains(@aria-label, 'Attach as a copy, Recipients get a copy to review.')]")
            )
        )

        browser.find_element_by_xpath("//button[contains(@aria-label, 'Attach as a copy, Recipients get a copy to review.')]").click()

        # Give the browser more time to upload the huge file
        longer_timeout = 45
    except TimeoutException:
        pass

    # Wait for image to be fully uploaded using a (potentially) longer timeout
    WebDriverWait(browser, longer_timeout).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//div[@aria-label='Content pane']//div[contains(@aria-label, '{filename}')]")
        )
    )

    # Outlook provides a URL to the file's attachment on their back-end when it is fully uploaded.
    WebDriverWait(browser, longer_timeout).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//div[@aria-label='Content pane']//img[contains(@src, 'https://attachments.office.net/owa/{username}')]")
        )
    )


def goto_sent_items():
    """
    Go to the sent items folder.
    """

    # Wait for the "Sent items" button to be visible.
    # Sometimes this action is done after a page refresh, so we might need to wait.
    sent_items_ref = '//*[@title="Sent Items"]'
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, sent_items_ref)
        )
    )

    # Click and wait until we see "sent" messages
    sent_emails_button = browser.find_element_by_xpath(sent_items_ref)
    sent_emails_button.click()
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.CLASS_NAME, 'RKJYnFQ991LYsw_styUw')
        )
    )


def goto_inbox():
    """
    Go to the user's inbox.
    Sometimes we get an alert from Outlook saying that our changes may not be saved;
    we can safely ignore it. We wait for a short time to make sure the popup doesn't appear.
    """
    browser.get('https://outlook.office.com/mail/inbox')
    try:
        WebDriverWait(browser, short_timeout).until(
            expected_conditions.alert_is_present()
        )

        alert = browser.switch_to.alert
        alert.accept()
    except TimeoutException:
        pass


def send_email():
    """
    Sends an e-mail by clicking the "Send" button.

    Assumes that the screen is width 800px or less as the "Send" button
    slightly changes on bigger screens.
    """
    
    # Send e-mail
    send_button = browser.find_element_by_xpath('//*[@title="Send"]')
    send_button.click()

    # If we can find the error badge, there's a problem. Otherwise, send!
    try:
        WebDriverWait(browser, short_timeout).until( 
            expected_conditions.presence_of_element_located( 
                (By.XPATH, error_message_ref)
            )
        )
        return False
    except Exception:
        return True
