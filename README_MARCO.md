# Install procedures
## Install dev version Odoo
To install Odoo to develop more modules you have to dollow the video below.
###### How to Configure Odoo With Pycharm - Odoo Mates
https://www.youtube.com/watch?v=p7SJW36lqVE
####Issues with odoo configuration
In the tutorial you have to get from zip or git clone the Repository of Odoo (https://github.com/odoo/odoo/).  
First of all keep attention to select from github page the branch of correct odoo version (in our case 12.0 https://github.com/odoo/odoo/tree/12.0).  
After this unzip the content and open with pycharm the folder extracted.

## Install this application 
First of all you need to install postgresql as shown in video.
You now need to install python libraries dependencies.  
I got some problem trying to run `pip install -r requirements.txt` however it could be useful this discussion about it https://stackoverflow.com/questions/41457612/how-to-use-requirements-txt-to-install-all-dependencies-in-a-python-project.


## Install Modules
To install this app you have to install correctly apps either in the default list of oddo APPS section then on custom app path.

* ###Deault App section apps
App name | Tecnical name | Notes
-------- | ------------- | -----
Invoicing | account |
Employees | hr |
Contacts | contacts | 
Discuss | mail | 
Calendar | calendar |
Italy accounting | l10n -italy | solves problem about contact creation
* ###other Module to install (if not done yet)
Module name | Tecnical name | Notes
-------- | ------------- | -----
Remove import button | display imort button | module get by 3rd party devs to remove from dashboards the import button
Account Bank Statement Import | account_bank_statement_import | Generic Wizard to Import Bank Statements (This module does not include any type of import format).OFX and QIF imports are available in Enterprise version.
Import Vendor Bills From XML | account_facturx
Tax Balance | account_tax_balance | https://github.com/OCA/account-financial-reporting
Analytic account | analytic | Module for defining analytic accounting object. In Odoo, analytic accounts are linked to general accounts but are treated totally independently. So, you can enter various different analytic operations that have no counterpart in the general financial accounts.
Signup | auth_signup | Allow users to sign up and reset their password
Base | base | The kernel of Odoo, needed for all installation.
IBAN Bank Accounts | base_iban | This module installs the base for IBAN (International Bank Account Number) bank accounts and checks for it's validity. The ability to extract the correctly represented local accounts from IBAN accounts with a single statement.
Base import | base_import | New extensible file import for Odoo. ** see module doc on Apps section for more info
Initial Setup Tools | base_setup | This module helps to configure the system at the installation of a new database. Shows you a list of applications features to install from.
VAT Number Validation | base_vat | VAT validation for Partner's VAT numbers. ** see module doc on Apps section for more info
IM Bus | bus | Instant Messaging Bus allow you to send messages to users, in live.
Calendar - SMS | calendar_sms | Send text messages as event reminders
Date range | date_range | This module lets you define global date ranges that can be used to filter your values in tree views. https://github.com/oca/server-ux
Decimal Precision Configuration | decimal_precision | Configure the price accuracy you need for different kinds of usage: accounting, sales, purchases.
KPI Digests | digest | Send KPI Digests periodically
Email Gateway | fetchmail | Retrieve incoming email on POP/IMAP servers. ** same above
Module for Calls activity management | gest_call | Calls activity management
In-App Purchases | iap | This module provides standard tools (account model, context manager and helpers) to support In-App purchases inside Odoo.
Multi Language Chart of Accounts | l10n_multilang | Multi language support for Chart of Accounts, Taxes, Tax Codes, Journals, Accounting Templates, Analytic Chart of Accounts and Analytic Journals.
OdooBot | mail_bot | https://www.odoo.com/page/discuss
Partner Autocomplete | partner_autocomplete | Auto-complete partner companies' data
Payment Acquirer | payment | Payment Acquirer Base Module
Transfer Payment Acquirer | payment_transfer | Transfer Payment Acquirer
Products & Pricelists | product | This is the base module for managing products and pricelists in Odoo. ** as above
Resource | resource | Module for resource management. A resource represent something that can be scheduled (a developer on a task or a work center on manufacturing orders). This module manages a resource calendar associated to every resource. It also manages the leaves of every resource.
SMS gateway | sms | This module gives a framework for SMS text messaging. The service is provided by the In App Purchase Odoo platform.
Snail Mail | snailmail | Allows users to send documents by post
snailmail_account | snailmail_account | Allows users to send invoices by post
Units of measure | uom | This is the base module for managing Units of measure.
Web | web | Odoo Web core module. This module provides the core of the Odoo Web Client.
Odoo Web Diagram | web_diagram | Openerp Web Diagram view.
Web Editor | web_editor | Odoo Web Editor widget.
Gauge Widget for Kanban | web_kanban_gauge | This widget allows to display gauges using d3 library.
Odoo Settings Dashboard | web_settings_dashboard | Odoo dashboard    Quick access to install apps    Quick users add    Quick access to the App Store and Theme Store
Tours | web_tour | Odoo Web tours.
Unsplash Image Library | web_unsplash | Find free high-resolution images from Unsplash
Web Timepicker Widget | web_widget_timepicker | This module provides a timepicker widget for float fields. It can be used as a replacement for the standard float_time widget in form views. https://github.com/OCA/web/
Customer Portal | portal | This module adds required base code for a fully integrated customer portal. It contains the base controller class and base templates. Business addons will add their specific templates and controllers to extend the customer portal. This module contains most code coming from odoo v10 website_portal. Purpose of this module is to allow the display of a customer portal without having a dependency towards website edition and customization capabilities.
Web Routing | http_routing | Proposes advanced routing options not available in web or base to keep base modules simple.
