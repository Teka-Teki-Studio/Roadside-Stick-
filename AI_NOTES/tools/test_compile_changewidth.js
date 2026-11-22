const path = require('path');
const libGD = require('./libGD.js');

libGD().then(gd => {
  const project = new gd.ProjectHelper.createNewGDJSProject();
  const layout = project.insertNewLayout('Test', 0);
  
  // Add Sprite object
  const obj = layout.insertNewObject(project, 'Sprite', 'Spr_LoadingBarFill', 0);
  
  // Create event with ChangeWidth
  const evt = layout.getEvents().insertNewEvent(project, 'BuiltinCommonInstructions::Standard', 0);
  const stdEvt = gd.asStandardEvent(evt);
  
  const act = new gd.Instruction();
  act.setType('ChangeWidth');
  act.setParametersCount(3);
  act.setParameter(0, 'Spr_LoadingBarFill');
  act.setParameter(1, '=');
  act.setParameter(2, '500');
  stdEvt.getActions().push_back(act);
  
  const gen = new gd.LayoutCodeGenerator(project);
  const includes = new gd.SetString();
  const diag = new gd.DiagnosticReport();
  
  const code = gen.generateLayoutCompleteCode(layout, includes, diag, false);
  console.log("COMPILED CODE TEST:");
  console.log(code);
  
  project.delete();
});
