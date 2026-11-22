const path = require('path');
const libGD = require('./libGD.js');

libGD().then(gd => {
  const platform = gd.JsPlatform.get();
  
  const candidateActions = [
    'Width', 'SetWidth', 'MettreLargeur', 'ScaleWidth', 'Scale', 'ScaleX', 
    'SetScale', 'SetScaleX', 'ModScale', 'ChangeWidth', 'ChangeScale',
    'Sprite::Width', 'Sprite::SetWidth', 'Sprite::ScaleWidth',
    'TiledSpriteObject::Width', 'TiledSpriteObject::SetWidth'
  ];

  console.log("=== CHECKING ACTION METADATA ===");
  for (const act of candidateActions) {
    const meta = gd.MetadataProvider.getActionMetadata(platform, act);
    const isBad = gd.MetadataProvider.isBadInstructionMetadata(meta);
    if (!isBad) {
      console.log(`VALID ACTION: "${act}" -> ParamCount: ${meta.getParametersCount()}, Description: "${meta.getDescription()}"`);
      for (let p = 0; p < meta.getParametersCount(); p++) {
        console.log(`   param ${p}: ${meta.getParameter(p).getName()} (${meta.getParameter(p).getType()})`);
      }
    }
  }

  // Also check all available actions on BaseObject and Sprite
  const ext = platform.getAllPlatformExtensions();
  for (let i = 0; i < ext.size(); i++) {
    const e = ext.at(i);
    const acts = e.getAllActions();
    const keys = acts.keys();
    for (let k = 0; k < keys.size(); k++) {
      const key = keys.at(k);
      if (key.toLowerCase().includes('width') || key.toLowerCase().includes('scale') || key.toLowerCase().includes('largeur') || key.toLowerCase().includes('size')) {
        console.log(`Ext [${e.getName()}]: "${key}"`);
      }
    }
  }
});
