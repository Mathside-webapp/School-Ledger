import {rm,mkdir,cp} from 'node:fs/promises';
await rm('dist',{recursive:true,force:true});
await mkdir('dist',{recursive:true});
await cp('web','dist',{recursive:true});
console.log('Offline browser assets copied to dist/. No external network dependencies.');
