import {createServer} from 'node:http';
import {readFile,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('../web/',import.meta.url)));
const types={'.html':'text/html;charset=utf-8','.css':'text/css;charset=utf-8','.js':'text/javascript;charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.ico':'image/x-icon','.json':'application/json'};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');const relative=decodeURIComponent(url.pathname).replace(/^\/+/, '')||'index.html';const path=resolve(root,relative);if(path!==root&&!path.startsWith(root+sep)){res.writeHead(403).end();return;}const content=await readFile(path);res.writeHead(200,{'Content-Type':types[extname(path)]||'application/octet-stream','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(content);}catch{res.writeHead(404).end('Not found');}});
server.listen(4173,'127.0.0.1',()=>console.log('CanteenLedger offline preview: http://127.0.0.1:4173'));
