// backend/services/emailService.js
// Email notifications for friend requests

const nodemailer = require('nodemailer');

// Email configuration from environment variables
const EMAIL_HOST = process.env.EMAIL_HOST || 'smtp.gmail.com';
const EMAIL_PORT = process.env.EMAIL_PORT || 587;
const EMAIL_USER = process.env.EMAIL_USER; // Your email
const EMAIL_PASS = process.env.EMAIL_PASS; // Your email password or app password
const EMAIL_FROM = process.env.EMAIL_FROM || process.env.EMAIL_USER;
const APP_URL = process.env.APP_URL || 'http://localhost:8080';
const APP_NAME = process.env.APP_NAME || 'MyMDB';

// Create transporter
const transporter = nodemailer.createTransporter({
  host: EMAIL_HOST,
  port: EMAIL_PORT,
  secure: EMAIL_PORT === 465, // true for 465, false for other ports
  auth: {
    user: EMAIL_USER,
    pass: EMAIL_PASS,
  },
});

// Verify transporter configuration
if (EMAIL_USER && EMAIL_PASS) {
  transporter.verify(function (error, success) {
    if (error) {
      console.error('Email transporter error:', error);
    } else {
      console.log('Email server is ready to send messages');
    }
  });
} else {
  console.warn('Email credentials not configured. Friend request emails will not be sent.');
}

/**
 * Send friend request notification email
 */
async function sendFriendRequestEmail(recipientEmail, recipientUsername, requesterUsername) {
  // Skip if email not configured
  if (!EMAIL_USER || !EMAIL_PASS) {
    console.log('Email not configured, skipping friend request notification');
    return;
  }

  const mailOptions = {
    from: `${APP_NAME} <${EMAIL_FROM}>`,
    to: recipientEmail,
    subject: `${requesterUsername} sent you a friend request on ${APP_NAME}`,
    html: `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
    }
    .container {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 30px;
      border: 1px solid #e0e0e0;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .logo {
      font-size: 32px;
      font-weight: bold;
      color: #1976D2;
      margin-bottom: 10px;
    }
    .content {
      background-color: white;
      padding: 25px;
      border-radius: 6px;
      margin-bottom: 20px;
    }
    .username {
      font-weight: bold;
      color: #1976D2;
    }
    .button {
      display: inline-block;
      padding: 12px 24px;
      margin: 10px 5px;
      background-color: #1976D2;
      color: white;
      text-decoration: none;
      border-radius: 4px;
      font-weight: 500;
    }
    .button:hover {
      background-color: #1565C0;
    }
    .button-secondary {
      background-color: #757575;
    }
    .button-secondary:hover {
      background-color: #616161;
    }
    .actions {
      text-align: center;
      margin: 25px 0;
    }
    .footer {
      text-align: center;
      font-size: 12px;
      color: #757575;
      margin-top: 20px;
    }
    .footer a {
      color: #1976D2;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">🎬 ${APP_NAME}</div>
    </div>
    
    <div class="content">
      <h2>New Friend Request</h2>
      <p>Hi <strong>${recipientUsername}</strong>,</p>
      <p>
        <span class="username">${requesterUsername}</span> wants to connect with you on ${APP_NAME}!
      </p>
      <p>
        Connect with friends to compare your movie ratings, discover shared favorites, 
        and see what everyone's watching.
      </p>
    </div>
    
    <div class="actions">
      <a href="${APP_URL}/friends/requests" class="button">View Request</a>
    </div>
    
    <div class="footer">
      <p>
        You're receiving this email because you have friend request notifications enabled.
      </p>
      <p>
        <a href="${APP_URL}/settings">Update your notification preferences</a>
      </p>
      <p style="margin-top: 15px; color: #999;">
        © ${new Date().getFullYear()} ${APP_NAME}. All rights reserved.
      </p>
    </div>
  </div>
</body>
</html>
    `,
    text: `
Hi ${recipientUsername},

${requesterUsername} sent you a friend request on ${APP_NAME}!

View and respond to this request at: ${APP_URL}/friends/requests

Connect with friends to compare movie ratings and see what everyone's watching.

---
You're receiving this email because you have friend request notifications enabled.
Update your preferences at: ${APP_URL}/settings

© ${new Date().getFullYear()} ${APP_NAME}
    `.trim()
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    console.log('Friend request email sent:', info.messageId);
    return info;
  } catch (error) {
    console.error('Error sending friend request email:', error);
    throw error;
  }
}

/**
 * Send friend request accepted notification (optional)
 */
async function sendFriendRequestAcceptedEmail(recipientEmail, recipientUsername, accepterUsername) {
  // Skip if email not configured
  if (!EMAIL_USER || !EMAIL_PASS) {
    return;
  }

  const mailOptions = {
    from: `${APP_NAME} <${EMAIL_FROM}>`,
    to: recipientEmail,
    subject: `${accepterUsername} accepted your friend request on ${APP_NAME}`,
    html: `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
    }
    .container {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 30px;
    }
    .content {
      background-color: white;
      padding: 25px;
      border-radius: 6px;
    }
    .button {
      display: inline-block;
      padding: 12px 24px;
      background-color: #1976D2;
      color: white;
      text-decoration: none;
      border-radius: 4px;
      margin-top: 15px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="content">
      <h2>🎉 ${accepterUsername} is now your friend!</h2>
      <p>Hi ${recipientUsername},</p>
      <p>
        Great news! <strong>${accepterUsername}</strong> accepted your friend request.
      </p>
      <p>
        You can now compare ratings, see their activity, and discover new movies together!
      </p>
      <div style="text-align: center;">
        <a href="${APP_URL}/friends/${accepterUsername}/compare" class="button">Compare Ratings</a>
      </div>
    </div>
  </div>
</body>
</html>
    `
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    console.log('Acceptance email sent:', info.messageId);
    return info;
  } catch (error) {
    console.error('Error sending acceptance email:', error);
  }
}

module.exports = {
  sendFriendRequestEmail,
  sendFriendRequestAcceptedEmail,
};