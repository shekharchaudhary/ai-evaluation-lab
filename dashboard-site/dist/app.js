const cases=[
['pb-001','factuality','A'],['pb-002','instruction following','A'],['pb-003','calibration','B'],['pb-004','completeness','A'],['pb-005','clarity','A'],['pb-006','safety','B'],['pb-007','relevance','A'],['pb-008','citation support','A'],['pb-009','conciseness','A'],['pb-010','reasoning','A'],['pb-011','ambiguity','B'],['pb-012','tie','TIE']
].map(([id,category,human])=>({id,category,human,ab:'—',ba:'—',flipped:null}));

const $=s=>document.querySelector(s);const body=$('#resultsBody');let running=false;
function render(filter='all'){
  const visible=cases.filter(c=>filter==='all'||(filter==='flipped'&&c.flipped)||(filter==='agreed'&&c.flipped===false));
  body.innerHTML=visible.map(c=>`<tr><td class="case-id">${c.id}</td><td><span class="pill">${c.category}</span></td><td class="verdict">${c.human}</td><td class="verdict">${c.ab}</td><td class="verdict">${c.ba}</td><td><span class="outcome ${c.flipped===null?'':c.flipped?'flipped':'stable'}">${c.flipped===null?'pending':c.flipped?'flipped':'stable'}</span></td></tr>`).join('');
}
function canonical(order){return order==='AB'?'A':'B'}
function setEvent(text){$('#eventStream').innerHTML=`<span>${text}</span>`}
function finish(){
  running=false;$('#statusBadge').textContent='Complete';$('#statusBadge').className='status complete';$('#runButton').disabled=false;$('#runButton span').textContent='Run again';
  $('#flipRate').textContent='100%';$('#flipInterval').textContent='95% bootstrap CI 100–100%';$('#firstPreference').textContent='100%';$('#preferenceMeter').style.width='100%';$('#agreementAB').textContent='66.7%';$('#agreementBA').textContent='25.0%';
  $('#interpretation').textContent='The harness correctly exposes the control’s complete dependence on presentation order.';
  $('#flippedCount').textContent='12';$('#stableCount').textContent='0';
  $('#flipBars').innerHTML=cases.map(()=>'<i class="hot" style="height:100%"></i>').join('');setEvent('Run complete · 12 / 12 cases changed verdict after order reversal');
}
async function run(){
  if(running)return;running=true;cases.forEach(c=>{c.ab='—';c.ba='—';c.flipped=null});render();
  $('#statusBadge').textContent='Running';$('#statusBadge').className='status running';$('#runButton').disabled=true;$('#runButton span').textContent='Evaluating…';
  $('#flipRate').textContent='—';$('#firstPreference').textContent='—';$('#agreementAB').textContent='—';$('#agreementBA').textContent='—';$('#progressFill').style.width='0%';
  let done=0;for(const c of cases){for(const order of ['AB','BA']){await new Promise(r=>setTimeout(r,120));const verdict=canonical(order);c[order.toLowerCase()]=verdict;done++;$('#progressFill').style.width=`${done/24*100}%`;$('#progressCount').textContent=`${done} / 24 judgments`;$('#progressLabel').textContent=`Judging ${c.id} · ${order} order`;setEvent(`${c.id} · ${order} → FIRST displayed response → canonical ${verdict}`);render();}c.flipped=c.ab!==c.ba;render();}
  finish();
}
$('#runButton').addEventListener('click',run);document.addEventListener('keydown',e=>{if(e.key.toLowerCase()==='r'&&!['INPUT','TEXTAREA'].includes(e.target.tagName))run()});
document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(x=>x.classList.remove('active'));button.classList.add('active');render(button.dataset.filter)}));
render();$('#flipBars').innerHTML=cases.map(()=>'<i style="height:18%"></i>').join('');
