# Comprehensive Onboarding Journey for TEMS Platform

---

### Phase 1: Customer Account Provisioning (The "Welcome")

*This phase covers the automated process from successful payment to the admin's first login.*

**Key Steps:**
1. **Payment Confirmation**: Automated receipt generation and acknowledgment
2. **Tenant/Site Creation**: Automatic provisioning of a dedicated Frappe site for the customer
3. **Database Setup**: Configuration of company-specific database with pre-loaded African country settings
4. **Initial Admin User Creation**: Creation of the primary administrator account with temporary credentials
5. **Basic Configuration**: Pre-configuration of essential settings based on the customer's country and subscription plan

**Communication:**
- **Welcome Email**: Simple, visually clean email with:
  - Clear subject line: "Welcome to TEMS - Your Account is Ready!"
  - Direct login link (single-click access)
  - Temporary password (clearly marked as temporary)
  - 3 bullet points highlighting what to do next
  - Support contact information with phone number (critical for African market)
  - Link to a 2-minute welcome video (hosted on a low-bandwidth optimized platform)

- **SMS Notification**: For regions with limited email access:
  - Brief message: "Your TEMS account is ready! Login at [link] with temporary password: [password]. Call [number] for help."

**Frappe-Specific Tools:**
- **API Hooks**: From payment gateway (Stripe, Mobile Money) to trigger provisioning
- **Background Jobs**: For site creation and database setup using `frappe.enqueue`
- **Standard Email Templates**: Customized with simplified language and clear CTAs
- **Multi-tenancy Framework**: Using Frappe's Sites architecture for customer isolation
- **SMS Integration**: Via Frappe's SMS module or custom API integration
- **Automated Setup Script**: Python script that configures initial settings based on country

---

### Phase 2: First-Time Admin User Setup (The "Guided Tour")

*This phase is the critical first-run experience for the company's administrator.*

**Key Steps:**
1. **Welcome Screen**: Simple, branded welcome message with a 30-second video overview
2. **Forced Password Change**: One-click password reset with visual strength indicator
3. **Essential Setup Wizard** (5 critical pieces of information):
   - Company Details (name, address, logo upload)
   - Basic Fleet Information (number and types of vehicles)
   - Currency and Payment Methods (including mobile money options)
   - Timezone and Working Hours
   - Primary Contact Information

4. **Interactive Tour**: Guided walkthrough of the 3 most important features
5. **First Win Setup**: Guided creation of the first vehicle or driver record

**Communication:**
- **In-App Pop-ups**: Simple, non-intrusive tooltips with "Next" buttons
- **Progress Checklist**: Visual checklist showing completion status (e.g., "3 of 5 completed")
- **Embedded Videos**: Short (under 90 seconds) task-specific videos with local language options
- **Contextual Help**: "?" icons next to complex fields with simple explanations
- **Success Celebrations**: Confetti animation when setup is complete

**Frappe-Specific Tools:**
- **Custom "Onboarding" DocType**: To track setup progress and trigger next steps
- **Web Forms**: For a simplified setup wizard with minimal fields per screen
- **Customized Desk Page**: Modified home page with onboarding checklist and quick actions
- **Frappe's Built-in Tour Feature**: Customized for the most important workflows
- **Client Scripts**: For form validation and progressive disclosure of complex options
- **Custom Notifications**: To guide users through the setup process
- **Image Upload Widget**: For logo upload with preview and cropping

---

### Phase 3: Inviting and Onboarding Team Members (The "Expansion")

*This phase focuses on how the admin gets their team onto the platform.*

**Key Steps:**
1. **Simple User Invitation Form**: Email address and role selection only
2. **Bulk Import Option**: CSV template download and upload for multiple users
3. **Role Assignment**: Simplified role selection with clear descriptions (e.g., "Fleet Manager: Can manage vehicles and drivers")
4. **Invited User Experience**: What new users see when they first log in
5. **Role-Specific Orientation**: Brief introduction based on user's permissions

**Communication:**
- **Invitation Email**: 
  - Subject: "[Admin Name] has invited you to join TEMS"
  - Clear login link and temporary password
  - 2-sentence description of what they'll be doing in TEMS
  - Link to a 60-second role-specific video
  - Support contact information

- **First-Login Experience for Non-Admin Users**:
  - Welcome message from the admin
  - Brief tour of their specific workspace (3 screens maximum)
  - Quick task related to their role (e.g., "Check your assigned vehicle")
  - Confirmation of successful login

**Frappe-Specific Tools:**
- **Standard "User" DocType**: With simplified fields for invitation
- **Role Profiles**: Pre-configured for common transport industry roles
- **Custom Scripts**: On the User form to trigger welcome emails and setup
- **Bulk Import Functionality**: Using Frappe's data import tool with custom templates
- **Permission Management**: Simplified permission sets based on roles
- **Custom Workspace Pages**: Role-specific desk views with relevant tools
- **Email Templates**: Customized for each user role
- **SMS Notifications**: For users in regions with limited email access

---

### Phase 4: Ongoing Engagement & Education (The "Adoption")

*This phase covers the first 7-14 days, designed to build habits and drive deeper adoption of features.*

**Key Steps:**
1. **Day 1-2**: Introduction to a secondary feature (e.g., basic reporting)
2. **Day 3-4**: Prompting for data import (e.g., existing vehicle/driver data)
3. **Day 5-7**: Highlighting a key report or dashboard that shows value
4. **Day 8-10**: Encouraging regular usage through personalized tips
5. **Day 11-14**: Collecting feedback and suggesting next steps

**Communication:**
- **Drip Email Campaign**:
  - Day 1: "Welcome to TEMS! Here's how to get started"
  - Day 3: "Did you know? You can track your vehicles in real-time"
  - Day 5: "See how much fuel you've saved this week"
  - Day 7: "3 tips to get more value from TEMS"
  - Day 10: "How are you finding TEMS? We'd love your feedback"

- **In-App Notifications**:
  - Contextual tips based on user behavior
  - Reminders for incomplete tasks
  - Celebrations of milestones (e.g., "You've logged 10 trips!")

- **Knowledge Base Links**:
  - Short, video-based tutorials (under 2 minutes)
  - Simple how-to guides with screenshots
  - FAQ section addressing common questions

**Frappe-Specific Tools:**
- **Notification System**: For in-app messages and alerts
- **Email Campaign Module**: For automated drip campaigns
- **Custom "Help & Resources" Desk Page**: With role-specific content
- **Analytics Dashboard**: To track user engagement and feature adoption
- **Custom Reports**: To show value and ROI to users
- **Feedback Forms**: Simple forms to collect user input
- **Scheduled Jobs**: To trigger communications based on user behavior
- **Custom Workspace Elements**: Highlighting new or underused features
- **Usage Tracking**: To personalize recommendations based on actual usage patterns

---

## Key Design Principles for Non-Technical Users

1. **Progressive Disclosure**: Only show what's necessary for the current task
2. **Visual Hierarchy**: Use size, color, and spacing to guide attention
3. **Consistent Language**: Use simple, consistent terminology throughout
4. **Error Prevention**: Design forms to prevent errors before they happen
5. **Immediate Feedback**: Show the results of actions immediately
6. **Minimal Cognitive Load**: Break complex tasks into small, manageable steps
7. **Accessibility**: Ensure the platform works well on low-end devices and poor connections
8. **Multilingual Support**: Provide content in major African languages

This onboarding journey is designed to be intuitive, reduce friction, and guide non-technical users to their "Aha!" moment as quickly as possible, while leveraging the powerful features of the Frappe Framework.