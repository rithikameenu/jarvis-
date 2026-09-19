import requests
import json

BASE = 'http://127.0.0.1:8000/api/v1'

print('--- 1. Testing Health ---')
r = requests.get(f'{BASE}/health')
assert r.status_code == 200, f'Health failed: {r.text}'
print('Health OK:', r.json().get('status'))

print('--- 2. Testing 2-Step Login ---')
r1 = requests.post(f'{BASE}/auth/login', json={'email':'analyst@finsecure.com','password':'AnalystPass123!'})
assert r1.status_code == 200 and r1.json().get('mfa_required'), f'Step 1 failed: {r1.text}'
print('Step 1 OK: MFA Required')

r2 = requests.post(f'{BASE}/auth/verify-mfa', json={'email':'analyst@finsecure.com','mfa_code':'123456'})
assert r2.status_code == 200, f'Step 2 failed: {r2.text}'
token = r2.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print('Step 2 OK: Token received for', r2.json().get('role'))

print('--- 3. Testing Fraud Alerts ---')
r_alerts = requests.get(f'{BASE}/fraud-alerts?limit=5', headers=headers)
assert r_alerts.status_code == 200, f'Alerts failed: {r_alerts.text}'
alerts = r_alerts.json()
print(f'Alerts OK: Retrieved {len(alerts)} alerts')

print('--- 4. Testing Live Transactions & Simulation ---')
r_sim = requests.post(f'{BASE}/transactions/simulate', json={'force_fraud': True}, headers=headers)
assert r_sim.status_code in (200, 201), f'Simulation failed: {r_sim.text}'
sim_tx = r_sim.json()
tx_id = sim_tx.get('id')
risk_score = sim_tx.get('risk_score')
print(f'Simulation OK: Created TX-{tx_id} with Risk Score {risk_score}')

print('--- 5. Testing Case Investigation ---')
r_inv = requests.get(f'{BASE}/investigation/1', headers=headers)
assert r_inv.status_code == 200, f'Investigation failed: {r_inv.text}'
dossier = r_inv.json()
print('Investigation OK:')
print('  Account Status:', dossier['account']['account_status'])
print('  Safety Rating:', dossier['account']['risk_rating'])
print('  Network Nodes:', dossier['network_graph']['total_nodes'])
resp_snippet = dossier['ai_explanation']['response'][:140].replace('\n', ' ')
print(f'  AI Response: {resp_snippet}...')

print('--- 6. Testing Compliance AI ---')
r_ai = requests.post(f'{BASE}/ai/investigate', json={'query': 'What is the rule for unsolicited credit cards?'}, headers=headers)
assert r_ai.status_code == 200, f'Compliance AI query failed: {r_ai.text}'
ai_res = r_ai.json()
print('Compliance AI OK: Evidence source =', ai_res.get('source', 'RAG'))
print('Evidence count =', len(ai_res.get('evidence', [])))

print('\n========================================')
print('SUCCESS: ALL DEPLOYMENT CHECKS PASSED!')
print('========================================')
