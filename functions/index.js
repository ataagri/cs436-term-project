const functions = require('firebase-functions/v1');
const admin = require('firebase-admin');
const nodemailer = require('nodemailer');

admin.initializeApp();

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'cs436.reactfastcontacts@gmail.com',
    pass: 'igcvgcutcsoxrkam'
  }
});

exports.sendWelcomeEmail = functions.auth.user().onCreate(async (user) => {
  const email = user.email;
  const mailOptions = {
    from: 'ReactFast Contacts <cs436.reactfastcontacts@gmail.com>',
    to: email,
    subject: 'Welcome to Our App!',
    html: `
      <h1>Welcome to Our App!</h1>
      <p>Thank you for joining our platform. We're excited to have you on board!</p>
      <p>Here are the things you can do within our app:</p>
      <ul>
        <li>Add new contacts</li>
        <li>Update or delete existing contacts</li>
        <li>See details of your contacts</li>
      </ul>
      <p>If you have any questions, feel free to contact our support team.</p>
    `
  };

  try {
    await transporter.sendMail(mailOptions);
    console.log(`Welcome email sent to ${email}`);
    return null;
  } catch (error) {
    console.error('Error sending welcome email:', error);
    return null;
  }
});