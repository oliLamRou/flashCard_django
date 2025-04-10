Absolutely — here’s a clear guide on when to run `makemigrations` and `migrate`, plus top warnings to avoid breaking your Django models 🛠️🔥

---

## ✅ When to Run `makemigrations` and `migrate`

### `makemigrations`
Use this **every time you change a model**:
- Add, remove, or rename a model
- Add, remove, or rename a model field
- Change field type (e.g. `CharField` → `TextField`)
- Change field options (e.g. `max_length`, `default`, `null=True`, etc.)
- Add relationships (`ForeignKey`, `ManyToMany`, etc.)

```bash
python manage.py makemigrations
```

Django will create a new migration file under your app’s `migrations/` directory.

---

### `migrate`
Use this **after `makemigrations`**, to apply those changes to the actual database.

```bash
python manage.py migrate
```

It updates your schema so the database structure matches your models.

---

## ⚠️ Top Warnings: Things That Can Break Your Models

These are changes that can **break your app or data** if you’re not careful:

### 1. ❌ **Removing a model or field with existing data**
- Deleting a model or field that has data will drop that data from the database.
- **Fix**: Consider backing up data, or using `null=True` before removing.

### 2. ❌ **Changing field types (e.g., `CharField → IntegerField`)**
- Can cause migration errors or **data loss** if existing data can’t convert cleanly.
- **Fix**: Use a data migration to convert values safely before switching the field type.

### 3. ❌ **Setting `null=False` on a field that already has `null` values**
- This will break migrations with `IntegrityError`.
- **Fix**: Either:
  - Provide a `default=...`
  - Clean up `null` values manually
  - Allow `null=True`

### 4. ❌ **Changing primary key field type or name**
- This will usually break foreign key relationships and downstream data.
- **Fix**: Avoid changing `id` fields unless starting fresh or you **really** know what you’re doing.

### 5. ⚠️ **Changing a `ForeignKey` or `OneToOneField` without updating `on_delete` behavior**
- Default behavior may not suit your app (e.g., deleting a User deletes Preferences).
- **Fix**: Always define `on_delete=models.CASCADE`, `SET_NULL`, etc. explicitly.

### 6. ❌ **Renaming fields or models without using the `--name` flag**
- Django may think it’s a new field, and delete old data.
- **Fix**: Use:
  ```bash
  python manage.py makemigrations --empty yourapp
  ```
  Then manually edit the migration file to rename instead of drop/recreate.

---

## 🧠 Pro Tip: Check your migration plan before applying

```bash
python manage.py showmigrations
python manage.py sqlmigrate yourapp 000X
```

This shows the SQL that will run — great for catching potential issues before they hit the DB.

---

Want a mini script or alias to auto run these when you detect model changes?