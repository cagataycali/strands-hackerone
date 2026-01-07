import os
import requests
import base64
from typing import Dict, Any
from strands import tool

@tool
def hackerone(action: str, program_handle: str = None, report_id: str = None, 
              page: int = 1, limit: int = 25, query: str = None) -> Dict[str, Any]:
    """
    HackerOne API integration for bug bounty hunting and security research.
    
    Actions:
    - programs: List available bug bounty programs
    - program_info: Get detailed information about a specific program
    - program_scope: Get scope details for a program
    - program_weaknesses: Get weaknesses for a program
    - hacktivity: List public disclosed reports (hacktivity feed)
    - my_reports: List your submitted reports
    - report_details: Get details of a specific report
    - create_report: Submit a new vulnerability report
    - balance: Get your current balance
    - earnings: List your bounty earnings
    - payouts: List your payout history
    
    Args:
        action: The HackerOne API action to perform
        program_handle: Program handle/slug (for program-specific actions)
        report_id: Report ID (for report-specific actions)
        page: Page number for paginated results (default: 1)
        limit: Number of results per page (default: 25, max: 100)
        query: Search query for hacktivity (Lucene syntax)
        
    Returns:
        Dict containing status and HackerOne API response data
    """
    try:
        api_key = os.environ.get('HACKERONE_API_KEY')
        
        if not api_key:
            return {
                "status": "error",
                "content": [{"text": "❌ HACKERONE_API_KEY environment variable not set"}]
            }
        
        # Try to auto-detect username from environment or use API key as username
        username = os.environ.get('HACKERONE_USERNAME')
        if not username:
            return {
                "status": "error",
                "content": [{"text": "❌ HACKERONE_USERNAME environment variable not set. Please set your HackerOne username."}]
            }
        
        # Create basic auth header
        credentials = f"{username}:{api_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json",
            "User-Agent": "strands-hackerone-tool/1.0"
        }
        
        base_url = "https://api.hackerone.com/v1"
        
        if action == "programs":
            url = f"{base_url}/hackers/programs"
            params = {
                "page[size]": min(limit, 100),
                "page[number]": page
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                programs = data.get('data', [])
                
                result = f"🎯 **Bug Bounty Programs (Page {page})**\n\n"
                result += f"**📊 Found:** {len(programs)} programs\n\n"
                
                for program in programs:
                    attrs = program.get('attributes', {})
                    handle = attrs.get('handle', 'Unknown')
                    name = attrs.get('name', 'Unknown')
                    state = attrs.get('state', 'Unknown')
                    submission_state = attrs.get('submission_state', 'Unknown')
                    offers_bounties = attrs.get('offers_bounties', False)
                    
                    result += f"**🏢 {name}**\n"
                    result += f"   Handle: {handle}\n"
                    result += f"   Status: {state}\n"
                    result += f"   Submissions: {submission_state}\n"
                    result += f"   Bounties: {'Yes' if offers_bounties else 'No'}\n\n"
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Programs list failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "program_info":
            if not program_handle:
                return {
                    "status": "error",
                    "content": [{"text": "❌ program_handle required for program_info"}]
                }
            
            url = f"{base_url}/hackers/programs/{program_handle}"
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                attrs = data.get('data', {}).get('attributes', {})
                
                result = f"🎯 **Program: {attrs.get('name', 'Unknown')}**\n\n"
                result += f"**Handle:** {attrs.get('handle', 'Unknown')}\n"
                result += f"**State:** {attrs.get('state', 'Unknown')}\n"
                result += f"**Submission State:** {attrs.get('submission_state', 'Unknown')}\n"
                result += f"**Started:** {attrs.get('started_accepting_at', 'Unknown')}\n"
                
                if attrs.get('offers_bounties'):
                    result += f"**💰 Bounties:** Yes\n"
                else:
                    result += f"**💰 Bounties:** No (Hall of Fame only)\n"
                
                if attrs.get('fast_payments'):
                    result += f"**⚡ Fast Payments:** Yes\n"
                
                if attrs.get('open_scope'):
                    result += f"**🔍 Open Scope:** Yes\n"
                
                # Policy excerpt
                policy = attrs.get('policy', '')
                if policy and len(policy) > 100:
                    policy_excerpt = policy[:200] + "..."
                    result += f"\n**📋 Policy Excerpt:**\n{policy_excerpt}\n"
                
                return {
                    "status": "success", 
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Program info failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "program_scope":
            if not program_handle:
                return {
                    "status": "error",
                    "content": [{"text": "❌ program_handle required for program_scope"}]
                }
            
            url = f"{base_url}/hackers/programs/{program_handle}/structured_scopes"
            params = {
                "page[size]": min(limit, 100),
                "page[number]": page
            }
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                scopes = data.get('data', [])
                
                result = f"🎯 **Program Scope: {program_handle}**\n\n"
                
                in_scope = [s for s in scopes if s.get('attributes', {}).get('eligible_for_bounty')]
                out_scope = [s for s in scopes if not s.get('attributes', {}).get('eligible_for_bounty')]
                
                if in_scope:
                    result += "**✅ IN SCOPE (Bounty Eligible):**\n"
                    for scope in in_scope[:100]:  # Show first 100
                        attrs = scope.get('attributes', {})
                        asset_type = attrs.get('asset_type', 'Unknown')
                        asset_identifier = attrs.get('asset_identifier', 'Unknown')
                        instruction = attrs.get('instruction', '')
                        max_severity = attrs.get('max_severity', 'Unknown')
                        
                        result += f"- {asset_type}: `{asset_identifier}` (Max: {max_severity})"
                        if instruction:
                            result += f" - {instruction}"
                        result += "\n"
                    result += "\n"
                
                if out_scope:
                    result += "**❌ OUT OF SCOPE:**\n"
                    for scope in out_scope[:100]:  # Show first 100
                        attrs = scope.get('attributes', {})
                        asset_type = attrs.get('asset_type', 'Unknown')
                        asset_identifier = attrs.get('asset_identifier', 'Unknown')
                        instruction = attrs.get('instruction', '')
                        
                        result += f"- {asset_type}: `{asset_identifier}`"
                        if instruction:
                            result += f" - {instruction}"
                        result += "\n"
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Program scope failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "program_weaknesses":
            if not program_handle:
                return {
                    "status": "error",
                    "content": [{"text": "❌ program_handle required for program_weaknesses"}]
                }
            
            url = f"{base_url}/hackers/programs/{program_handle}/weaknesses"
            params = {
                "page[size]": min(limit, 100),
                "page[number]": page
            }
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                weaknesses = data.get('data', [])
                
                result = f"🔍 **Program Weaknesses: {program_handle}**\n\n"
                result += f"**📊 Available Types:** {len(weaknesses)}\n\n"
                
                for weakness in weaknesses:
                    attrs = weakness.get('attributes', {})
                    name = attrs.get('name', 'Unknown')
                    external_id = attrs.get('external_id', '')
                    description = attrs.get('description', '')
                    
                    result += f"**{name}** ({external_id})\n"
                    if description and len(description) > 50:
                        desc_excerpt = description[:100] + "..."
                        result += f"   {desc_excerpt}\n"
                    result += "\n"
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Program weaknesses failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "hacktivity":
            url = f"{base_url}/hackers/hacktivity"
            params = {
                "page[size]": min(limit, 100),
                "page[number]": page
            }
            if query:
                params["queryString"] = query
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                activities = data.get('data', [])
                
                result = f"🔥 **HackerOne Hacktivity (Page {page})**\n\n"
                if query:
                    result += f"**🔍 Query:** {query}\n"
                result += f"**📊 Recent Disclosures:** {len(activities)}\n\n"
                
                for activity in activities:
                    attrs = activity.get('attributes', {})
                    title = attrs.get('title') or 'Undisclosed'
                    disclosed_at = attrs.get('disclosed_at') or 'Not disclosed'
                    severity = attrs.get('severity_rating') or 'Unknown'
                    bounty = attrs.get('total_awarded_amount') or 0
                    
                    # Get program info from relationships (handle null values)
                    relationships = activity.get('relationships', {})
                    program_data = relationships.get('program', {}).get('data', {})
                    program_attrs = program_data.get('attributes', {}) if program_data else {}
                    program_handle = program_attrs.get('handle', 'Unknown')
                    
                    # Only show disclosed reports with titles
                    if title != 'Undisclosed':
                        result += f"**🎯 {title}**\n"
                        result += f"   Program: {program_handle}\n"
                        result += f"   Severity: {severity}\n"
                        result += f"   Bounty: ${bounty}\n"
                        result += f"   Disclosed: {disclosed_at[:10] if disclosed_at != 'Not disclosed' else 'Not disclosed'}\n\n"
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Hacktivity failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "my_reports":
            url = f"{base_url}/hackers/me/reports"
            params = {
                "page[size]": min(limit, 100),
                "page[number]": page
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                reports = data.get('data', [])
                
                result = f"📋 **My Reports (Page {page})**\n\n"
                result += f"**📊 Total Reports:** {len(reports)}\n\n"
                
                for report in reports:
                    attrs = report.get('attributes', {})
                    title = attrs.get('title', 'Untitled')
                    state = attrs.get('state', 'Unknown')
                    created_at = attrs.get('created_at', 'Unknown')
                    
                    # Get program info from relationships
                    relationships = report.get('relationships', {})
                    program_data = relationships.get('program', {}).get('data', {})
                    program_attrs = program_data.get('attributes', {})
                    program_handle = program_attrs.get('handle', 'Unknown')
                    
                    result += f"**🐛 {title}**\n"
                    result += f"   ID: {report.get('id', 'Unknown')}\n"
                    result += f"   Program: {program_handle}\n"
                    result += f"   State: {state}\n"
                    result += f"   Created: {created_at[:10] if created_at != 'Unknown' else 'Unknown'}\n"
                    result += "\n"
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ My reports failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "report_details":
            if not report_id:
                return {
                    "status": "error", 
                    "content": [{"text": "❌ report_id required for report_details"}]
                }
            
            url = f"{base_url}/hackers/reports/{report_id}"
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                attrs = data.get('data', {}).get('attributes', {})
                
                result = f"🐛 **Report Details**\n\n"
                result += f"**ID:** {report_id}\n"
                result += f"**Title:** {attrs.get('title', 'Unknown')}\n"
                result += f"**State:** {attrs.get('state', 'Unknown')}\n"
                result += f"**Created:** {attrs.get('created_at', 'Unknown')[:10]}\n"
                
                # Get severity from relationships
                relationships = data.get('data', {}).get('relationships', {})
                severity_data = relationships.get('severity', {}).get('data', {})
                if severity_data:
                    severity_attrs = severity_data.get('attributes', {})
                    result += f"**Severity:** {severity_attrs.get('rating', 'Unknown')}\n"
                
                # Vulnerability info excerpt (only visible if you own the report)
                vuln_info = attrs.get('vulnerability_information', '')
                if vuln_info and len(vuln_info) > 100:
                    vuln_excerpt = vuln_info[:300] + "..."
                    result += f"\n**🔍 Vulnerability Info:**\n{vuln_excerpt}\n"
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Report details failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "balance":
            url = f"{base_url}/hackers/payments/balance"
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                balance = data.get('data', {}).get('balance', 0)
                
                result = f"💰 **Current Balance**\n\n"
                result += f"**Balance:** ${balance:,}\n"
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Balance failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "earnings":
            url = f"{base_url}/hackers/payments/earnings"
            params = {
                "page[size]": min(limit, 100),
                "page[number]": page
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                earnings = data.get('data', [])
                
                result = f"💰 **My Earnings (Page {page})**\n\n"
                result += f"**📊 Recent Earnings:** {len(earnings)}\n\n"
                
                total_earned = 0
                for earning in earnings:
                    attrs = earning.get('attributes', {})
                    amount = attrs.get('amount', 0)
                    created_at = attrs.get('created_at', 'Unknown')
                    earning_type = earning.get('type', 'Unknown')
                    
                    total_earned += amount
                    
                    # Get program info from relationships
                    relationships = earning.get('relationships', {})
                    program_data = relationships.get('program', {}).get('data', {})
                    program_attrs = program_data.get('attributes', {})
                    program_handle = program_attrs.get('handle', 'Unknown')
                    
                    result += f"**💵 ${amount}**\n"
                    result += f"   Type: {earning_type}\n"
                    result += f"   Program: {program_handle}\n"
                    result += f"   Date: {created_at[:10] if created_at != 'Unknown' else 'Unknown'}\n\n"
                
                result = f"💰 **Total on Page:** ${total_earned:,}\n\n" + result
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Earnings failed: {response.status_code} - {response.text}"}]
                }
        
        elif action == "payouts":
            url = f"{base_url}/hackers/payments/payouts"
            params = {
                "page[size]": min(limit, 100),
                "page[number]": page
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                payouts = data.get('data', [])
                
                result = f"💳 **My Payouts (Page {page})**\n\n"
                result += f"**📊 Recent Payouts:** {len(payouts)}\n\n"
                
                total_paid = 0
                for payout in payouts:
                    amount = payout.get('amount', 0)
                    paid_out_at = payout.get('paid_out_at', 'Unknown')
                    payout_provider = payout.get('payout_provider', 'Unknown')
                    status = payout.get('status', 'Unknown')
                    reference = payout.get('reference', 'Unknown')
                    
                    total_paid += amount
                    
                    result += f"**💳 ${amount}**\n"
                    result += f"   Provider: {payout_provider}\n"
                    result += f"   Status: {status}\n"
                    result += f"   Reference: {reference}\n"
                    result += f"   Paid: {paid_out_at[:10] if paid_out_at != 'Unknown' else 'Unknown'}\n\n"
                
                result = f"💳 **Total on Page:** ${total_paid:,}\n\n" + result
                
                return {
                    "status": "success",
                    "content": [{"text": result}]
                }
            else:
                return {
                    "status": "error",
                    "content": [{"text": f"❌ Payouts failed: {response.status_code} - {response.text}"}]
                }
        
        else:
            return {
                "status": "error",
                "content": [{"text": f"❌ Unknown action: {action}. Available: programs, program_info, program_scope, program_weaknesses, hacktivity, my_reports, report_details, balance, earnings, payouts"}]
            }
    
    except Exception as e:
        return {
            "status": "error",
            "content": [{"text": f"❌ HackerOne tool error: {str(e)}"}]
        }