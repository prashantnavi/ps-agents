**User Stories, Acceptance Criteria, and Product Specifications for Account Management System**  

---

### User Story 1: Account Creation  
**As a** user,  
**I want to** create an account,  
**So that** I can manage my trading activities.  

**Acceptance Criteria:**  
- The system must allow users to enter a username and password during the account creation process.  
- The username must be unique.  
- The password must meet security standards (minimum of 8 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character).  
- Upon successful account creation, the user should receive a confirmation message.  

---

### User Story 2: Deposit Funds  
**As a** user,  
**I want to** deposit funds into my account,  
**So that** I can trade shares.  

**Acceptance Criteria:**  
- The system must allow users to specify an amount to deposit.  
- The deposit amount must be a positive value.  
- The system must update the account balance after the deposit is made.  
- A success message should confirm the deposit.  

---

### User Story 3: Withdraw Funds  
**As a** user,  
**I want to** withdraw funds from my account,  
**So that** I can access my investment profits.  

**Acceptance Criteria:**  
- The system must allow users to specify an amount to withdraw.  
- The withdrawal amount must not exceed the current account balance.  
- The system must update the account balance after the withdrawal is made.  
- An error message must be displayed if the withdrawal would result in a negative balance.  
- A success message should confirm the withdrawal.  

---

### User Story 4: Buy Shares  
**As a** user,  
**I want to** record buying shares of a company,  
**So that** I can build my investment portfolio.  

**Acceptance Criteria:**  
- The system must allow users to specify the share symbol (AAPL, TSLA, GOOGL) and the quantity they want to buy.  
- The system must check that the total cost of the shares does not exceed the account balance.  
- Upon successful purchase, the system must update the portfolio and account balance.  
- An error message must be displayed if trying to buy more shares than affordable.  
- A success message should confirm the share purchase.  

---

### User Story 5: Sell Shares  
**As a** user,  
**I want to** record selling shares,  
**So that** I can realize profits or cut losses.  

**Acceptance Criteria:**  
- The system must allow users to specify the share symbol and the quantity they want to sell.  
- The system must check that the user has enough shares to sell.  
- Upon successful sale, the system must update the portfolio and account balance.  
- An error message must be displayed if trying to sell shares that the user doesn't own.  
- A success message should confirm the share sale.  

---

### User Story 6: Calculate Portfolio Value  
**As a** user,  
**I want to** see the total value of my portfolio,  
**So that** I can make informed trading decisions.  

**Acceptance Criteria:**  
- The system must calculate the portfolio value based on current share prices for all shares held.  
- The calculation must include unrealized profits or losses compared to the initial deposit.  
- A report should display the total portfolio value and profit/loss figures.  

---

### User Story 7: Report Holdings  
**As a** user,  
**I want to** view my current holdings,  
**So that** I can track my investments at any time.  

**Acceptance Criteria:**  
- The system must display a list of shares currently held, including the quantity of each share and total value.  
- The report should be accessible at any time.  

---

### User Story 8: Report Profit/Loss  
**As a** user,  
**I want to** check my profit or loss,  
**So that** I can evaluate my trading performance.  

**Acceptance Criteria:**  
- The system must display the total profit/loss for all trades at any given time.  
- This should be calculated against the initial deposit and include both realized and unrealized profits/losses.  

---

### User Story 9: List Transactions  
**As a** user,  
**I want to** view my transaction history,  
**So that** I can keep track of my trading activities.  

**Acceptance Criteria:**  
- The system must list all transactions including deposits, withdrawals, purchases, and sales.  
- Each entry must include the type of transaction, amount, share symbols, and timestamps.  
- The transaction history should be accessible at any time.  

---

### User Story 10: Ensure Negative Balance Prevention  
**As a** user,  
**I want to** be protected from negative balances,  
**So that** I do not incur debt from trading activities.  

**Acceptance Criteria:**  
- The system must prevent withdrawal requests that exceed the current balance.  
- The system must check available funds during purchase requests to avoid overdraft.  
- The user should receive clear instructions when attempting actions that would result in a negative balance.  

---

### Integration with get_share_price(symbol)  
**Acceptance Criteria for Share Price Functionality:**  
- The system must utilize the get_share_price(symbol) function to retrieve current share prices for AAPL, TSLA, and GOOGL.  
- The returned prices must be used for all purchase/sale calculations.  

---

### Product Specifications Summary  
- The system will feature a user-friendly web interface for all account management activities.  
- All financial transactions must be processed securely, adhering to data protection regulations.  
- Testing will include unit tests for all functions, integration tests for system interactions, and user acceptance testing (UAT) for overall user experience.  

---