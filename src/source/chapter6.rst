Chapter 6. Building a Yahoo Answer's like site
--------------------------------------------------
(Topics introduced: Transactions, Middleware, Permissions, Messages.)

Diving in. [Code listing]  
  
Transactions. (Till previous chapters we were not using transactions and all database actions were in Autocommit mode. Here we want many views to work as part of a transaction.)
  Using TransactionMiddleware  to tie Http requests to transactions.
  Finer grained control over transaction using commit_manually
  
Permissions. (We would define various user levels, and different user levels have different permissions)
  Introducing permissions.
  Creating cutsom permissions.
  How Groups, Users and permissions work together.
  Using permission_required decorator.
  
Message. (For example when the user gets a reply to her question.)
  Using get_and_delete_messages()
  
