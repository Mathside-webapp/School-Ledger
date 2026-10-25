# CanteenLedger v3 — School Canteen & Cooperative Cash

Complete **offline-first** school canteen financial record app, compatible with desktop browsers and Android through Capacitor. Records stay on the current device in IndexedDB. No account or cloud database is required.

## What changed in v3

**Simple sales:** On **Record Sale**, enter only **date**, **Foods / Goods**, and **total money received in pesos**. Product names and optional remarks have been removed from the sales form. There is no product name, remarks, quantity, unit price, line-total, or Products page. Every sales entry goes into either the Food or Goods fund.

**Expenses paid from a chosen fund:** On **Expenses**, enter a date, amount, description, expense category, and **Paid from: Foods, Goods, or Cooperative Money**. This subtracts the amount from exactly one chosen fund. It also reduces overall available cash. The ledger, transaction details, and expense report identify the source fund.

**Cooperative Money:** In the new dedicated panel, **Add / subtract money** records deposits, withdrawals, and optional related members. **Add member** records a name and optional role. Edit or **Remove** members; removal hides them from active selection but retains their information and transaction history for accountability. Removed members can be restored.

**Four displayed balances:** Foods, Goods, Cooperative Money, and **Unassigned (older records)**. Older v1 transactions lacking a source remain in Unassigned instead of being assigned to a different fund without your permission. Your original sales, expense, receipt, audit, and report history is preserved. Old product catalog data is retained inside backups but is no longer edited in the UI.

**Financial terms:** Sales are total money received; expenses are money paid; cash movement is money in minus money out (including Coop and adjustments). **Expenses do not change historical sales totals.** They reduce the fund balance and overall available cash. Net cash movement is **not** accounting profit.

**Mobile navigation:** All nine pages appear on the bottom bar on narrow screens. Swipe horizontally to access Weekly Tracker, Monthly Tracker, Ledger, Coop, Reports, and Settings. There is no More popup. Desktop sidebar remains unchanged.

**Sales history preservation:** New entries are automatically titled Foods sales or Goods sales. Existing custom sale descriptions/remarks remain in prior transactions and backups. Corrections preserve original descriptions in the audit trail.

### Example

| Operation | Foods | Goods | Coop | All cash |
|---|---:|---:|---:|---:|
| Foods sales +₱2,500 | ₱2,500 | ₱0 | ₱0 | ₱2,500 |
| Goods sales +₱500 | ₱2,500 | ₱500 | ₱0 | ₱3,000 |
| Ingredients paid from Foods −₱800 | ₱1,700 | ₱500 | ₱0 | ₱2,200 |
| Coop deposit +₱1,000 | ₱1,700 | ₱500 | ₱1,000 | ₱3,200 |
| Repairs paid from Coop −₱300 | ₱1,700 | ₱500 | ₱700 | **₱2,900** |

All monetary values are stored as **integer centavos**. Corrections keep an audit trail. Reversals offset the same original fund. Cooperative payments and sales are distinct types so Coop money does not inflate sales reports.

## Run locally as a standalone website

1. Extract the complete ZIP into a folder.
2. Open `index.html` to start `web/index.html` directly.
3. If your browser blocks IndexedDB from `file://`, run the included `run-browser.bat` on Windows, or `sh run-browser.sh` on macOS/Linux (requires Node.js). This opens a local offline server; internet is not required.
4. In **Settings**, use **Download JSON backup** regularly. Restoring a backup replaces current records after a confirmation.

## Build an Android APK without Android Studio

1. Create a GitHub repository. Upload **the contents of the extracted ZIP**, including hidden `.github/workflows/build-android.yml`, into the repository root, rather than uploading only the ZIP.
2. Open **Actions → Build CanteenLedger Android APK → Run workflow**.
3. After a successful run, open **Artifacts → CanteenLedger-Debug-APK** and extract `app-debug.apk` from the artifact ZIP.
4. Transfer APK to Android and install it, allowing installation from your chosen file manager when prompted.

The workflow runs `npm test`, packages static assets, generates Capacitor Android, and compiles `assembleDebug` using GitHub's Android SDK. Android device compilation has not yet been verified in this environment. This is a debug APK for testing, not Play Store distribution. Debug signing keys can change across GitHub runs; **export a JSON backup before uninstalling the app or replacing an incompatible APK**. Removing the app can erase all locally stored records.

For local Android builds (requires Node.js, JDK, Android SDK):

```bash
npm install
npm test
npm run build
npx cap add android
npx cap sync android
python3 tools/patch_android.py
cd android
./gradlew assembleDebug
```

Use `gradlew.bat assembleDebug` on Windows. APK path is `android/app/build/outputs/apk/debug/app-debug.apk`.

## Reports, security, and limitations

Dashboard, weekly, monthly, ledger, expense and item-sales reports use the same offline transaction data. Reports export CSV, Excel XLSX, or PDF without internet access. Expense and transaction reports include the **fund**. Report summaries include each fund's closing cash amount.

Light/dark modes, optional PIN, offline receipts, backup/restore, end-of-day cash count, and historical audit logs remain. PIN is a **convenience lock**, not encryption or biometrics. Local data are not synchronized between devices. For formal financial reporting, reconcile physical cash and download backups regularly.

**Tests:** 14 Node unit tests cover centavo arithmetic, separate fund cash tracking, expense deduction, Coop deposits/withdrawals, reversal, legacy backup migration, and date boundaries. Chromium smoke tests cover sales, expense source, adding/removing members, Coop entries, running balance, XLSX/CSV/PDF export, and desktop/mobile layout using a mocked IndexedDB implementation. Actual persistence after a phone restart and full APK build require separate device/GitHub testing.
