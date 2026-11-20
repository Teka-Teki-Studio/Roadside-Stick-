const libGD = require('C:\\Users\\ASUS\\.gemini\\antigravity\\brain\\29446708-9512-473e-8ad5-01a604faa9f5\\scratch\\libGD_extracted.js');

libGD().then(gd => {
  const platform = gd.JsPlatform.get();
  const project = new gd.ProjectHelper.createNewGDJSProject();
  const layout = project.insertNewLayout('TestLayout', 0);
  
  // Add Player sprite object
  const player = layout.insertNewObject(project, 'Sprite', 'Player', 0);
  layout.getVariables().insertNew('high_score', 0).setValue(0);
  
  const psc = gd.ProjectScopedContainers.makeNewProjectScopedContainersForProjectAndLayout(project, layout);

  function testInstruction(type, params, isCond) {
    const inst = new gd.Instruction();
    inst.setType(type);
    for (let i = 0; i < params.length; i++) {
      inst.setParameter(i, params[i]);
    }
    const meta = isCond ? gd.MetadataProvider.getConditionMetadata(platform, type) : gd.MetadataProvider.getActionMetadata(platform, type);
    console.log('\nTesting', type, JSON.stringify(params));
    for (let p = 0; p < params.length; p++) {
      const res = gd.InstructionValidator.validateParameter(platform, psc, inst, meta, p);
      console.log(' Param ' + p + ' (' + params[p] + '): valid=' + res.isValid());
      res.delete();
    }
    inst.delete();
  }

  testInstruction('PlaySound', ['', 'assets/audio/sfx_pause.wav', 'no', '70', '1'], false);
  testInstruction('PlaySound', ['', '"assets/audio/sfx_pause.wav"', 'no', '70', '1'], false);
  testInstruction('EcrireFichierExp', ['"StickScavengerSave"', '"high_score"', 'Variable(high_score)'], false);
  testInstruction('LireFichierExp', ['"StickScavengerSave"', '"high_score"', '', 'high_score'], false);
  testInstruction('GroupExists', ['"StickScavengerSave"', '"high_score"'], true);
  testInstruction('ChangeColor', ['Player', '"255;100;100"'], false);
  testInstruction('Opacity', ['Player', '=', '255'], false);
});
