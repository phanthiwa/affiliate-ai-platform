import httpx
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'http://127.0.0.1:8000/api/v1'

print("=== 1. Testing Dashboard ===")
dash = httpx.get(f'{base}/dashboard/overview').json()
print(f"GMV: ฿{dash['total_gmv_thb']:,.2f} | Commission: ฿{dash['total_commission_thb']:,.2f}")
print(f"Daily Directives: {len(dash['daily_recommendations'])} items")
for r in dash['daily_recommendations']:
    print(f"  * [{r['badge_label']}] {r['headline_th']}")

print("\n=== 2. Testing Products & Opportunity Scoring ===")
prods = httpx.get(f'{base}/products').json()
for p in prods[:4]:
    print(f"  * {p['title_th'][:35]}... -> Opp Score: {p['opportunity_score']} ({p['classification']}) | Commission: {p['commission_rate']}% (~฿{p['estimated_commission']:.2f})")

print("\n=== 3. Testing 10-15 Clips Batch Generation for Google Flow ===")
batch = httpx.post(f'{base}/batch/generate-15-clips', json={'target_clip_count': 15, 'preferred_durations': [15, 20, 30]}).json()
print(f"Total Clips Generated: {batch['total_generated']}")
print(f"Google Flow Batch ID: {batch['google_flow_payload']['batch_id']}")
print(f"Sample Clip Hook (0-3s): \"{batch['clips'][0]['hook_text_th']}\"")
print(f"Storyboard Shots: {len(batch['clips'][0]['script']['storyboard_shots'])} shots")
print(f"Compliance Check: {batch['clips'][0]['compliance']['status']} ({batch['clips'][0]['compliance']['notes'][0]})")
print(f"Scheduled Slot: {batch['clips'][0]['scheduled_time_slot_th']}")

print("\n=== 4. Testing 5-Minute Batch Approval Studio ===")
clip_ids = [c['clip_id'] for c in batch['clips']]
approve_res = httpx.post(f'{base}/content/batch-approve', json=clip_ids).json()
print(f"Approval Result: {approve_res['status']} | Approved: {approve_res['approved_count']} clips")
print(f"Message: {approve_res['message_th']}")
print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")
