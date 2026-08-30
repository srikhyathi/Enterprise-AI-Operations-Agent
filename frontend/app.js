async function api(url,opt={}){let r=await fetch(url,opt);if(!r.ok)throw Error(await r.text());return r.json()}
const pct=x=>Number(x).toFixed(1)+"%";
async function metrics(){let m=await api("/metrics");cpu.textContent=pct(m.cpu_usage_percent);memory.textContent=pct(m.memory_usage_percent);disk.textContent=pct(m.disk_usage_percent)}
async function health(){try{await api("/health");healthEl=document.getElementById("health");healthEl.textContent="● System Healthy";healthEl.className="pill ok"}catch(e){}}
async function analyze(){analysis.textContent="Analyzing...";try{let d=await api("/ai/analyze"),r=d.root_cause_analysis;analysis.textContent="Mode: "+d.analysis_mode+"\n\nFindings:\n• "+r.findings.join("\n• ")+"\n\nRecommendations:\n• "+r.recommendations.join("\n• ")}catch(e){analysis.textContent=e.message}}
async function loadLogs(){let d=await api("/logs");logs.textContent=`Errors: ${d.total_errors}\nWarnings: ${d.total_warnings}\n\n${d.errors.join("\n")}\n\n${d.warnings.join("\n")}`}
async function loadIncidents(){let d=await api("/incidents");count.textContent=d.incidents.length;if(!d.incidents.length){incidents.textContent="No incidents stored.";return}incidents.innerHTML=d.incidents.map(i=>`<div class="incident"><b>${i.incident_number} — ${i.message}</b><div class="meta">Severity: ${i.severity} | Status: ${i.status} | ${i.created_at}</div><div>${(i.root_cause||[]).map(x=>"• "+x).join("<br>")}</div>${i.status==="OPEN"?`<button onclick="approve(${i.id})">Approve</button>`:""}${i.status==="APPROVED"?`<button onclick="remediate(${i.id})">Run Safe Remediation</button>`:""}${i.status==="INVESTIGATING"?`<button onclick="verify(${i.id})">Verify</button>`:""}</div>`).join("")}
async function createIncidents(){let d=await api("/incidents/create",{method:"POST"});alert("Created "+d.count+" incident(s)");loadIncidents()}
async function approve(id){await api(`/incidents/${id}/approve`,{method:"POST"});loadIncidents()}
async function remediate(id){if(confirm("Run safe demo remediation?")){let d=await api(`/incidents/${id}/remediate`,{method:"POST"});alert(d.result);loadIncidents()}}
async function verify(id){let d=await api(`/incidents/${id}/verify`,{method:"POST"});alert("Verification: "+d.verification);loadIncidents()}
async function refresh(){await Promise.all([metrics(),health(),loadLogs(),loadIncidents()])}refresh();setInterval(refresh,10000)
