from django.db import migrations, models


def merge_notes_into_why(apps, schema_editor):
    Task = apps.get_model('planner', 'Task')
    for task in Task.objects.all().iterator():
        notes = (task.notes or '').strip()
        if not notes:
            continue
        why = (task.why or '').strip()
        task.why = f'{why} — {notes}' if why else notes
        task.save(update_fields=['why'])


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='why',
            field=models.TextField(blank=True),
        ),
        migrations.RunPython(merge_notes_into_why, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='task',
            name='notes',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='est_time',
            new_name='estimation',
        ),
    ]