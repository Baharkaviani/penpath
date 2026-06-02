from celery import shared_task


@shared_task
def process_scan(scan_id: int):
    """OCR stub — sets review status with mock draft matching flowboard shape."""
    from .models import ScanUpload

    scan = ScanUpload.objects.filter(pk=scan_id).first()
    if not scan:
        return

    scan.status = ScanUpload.STATUS_PROCESSING
    scan.save(update_fields=['status'])

    scan.ocr_raw = {
        'draft': {
            'focus': 'Imported from scan (review)',
            'prize': '',
            'coreTasks': [
                {'goal': 'Review OCR row 1', 'why': '', 'time': '', 'notes': '', 'trackerFilled': 8},
            ]
            + [{'goal': '', 'why': '', 'time': '', 'notes': '', 'trackerFilled': 0}] * 6,
            'sideTasks': [{'goal': '', 'why': '', 'time': '', 'notes': '', 'trackerFilled': 0}] * 5,
            'flameRatings': {
                'focus': 3,
                'leverage': 3,
                'alignment': 3,
                'momentum': 3,
                'energy': 3,
                'fulfillment': 3,
            },
            'reflection': ['', '', '', ''],
        },
        'note': 'Stub OCR — configure GOOGLE_APPLICATION_CREDENTIALS for Vision API.',
    }
    scan.status = ScanUpload.STATUS_REVIEW
    scan.save(update_fields=['status', 'ocr_raw'])
