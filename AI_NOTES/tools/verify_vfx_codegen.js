const libGD = require('./libGD.js');

libGD().then(gd => {
  const p = gd.JsPlatform.get();
  const project = new gd.ProjectHelper.createNewGDJSProject();
  const layout = project.insertNewLayout('Test', 0);
  
  const ev = layout.getEvents().insertNewEvent(project, 'BuiltinCommonInstructions::Standard', 0);
  const stdEv = gd.asStandardEvent(ev);
  
  const act1 = new gd.Instruction();
  act1.setType('SetCameraX');
  act1.setParametersCount(5);
  act1.setParameter(0, '');
  act1.setParameter(1, '=');
  act1.setParameter(2, '512 + 4 * sin(10)');
  act1.setParameter(3, '""');
  act1.setParameter(4, '0');
  stdEv.getActions().push_back(act1);

  const act2 = new gd.Instruction();
  act2.setType('SetX');
  act2.setParametersCount(3);
  act2.setParameter(0, 'Spr');
  act2.setParameter(1, '=');
  act2.setParameter(2, '48 + 3 * sin(TimeFromStart() * 1.5)');
  stdEv.getActions().push_back(act2);

  const act3 = new gd.Instruction();
  act3.setType('ChangeOpacity');
  act3.setParametersCount(3);
  act3.setParameter(0, 'Btn');
  act3.setParameter(1, '=');
  act3.setParameter(2, '220 + 35 * sin(TimeFromStart() * 2.5)');
  stdEv.getActions().push_back(act3);

  // Add dummy objects
  const obj1 = layout.insertNewObject(project, 'Sprite', 'Spr', 0);
  const obj2 = layout.insertNewObject(project, 'Sprite', 'Btn', 0);

  const eventsFunctionsExtension = project.insertNewEventsFunctionsExtension('TestExt', 0);
  const game = new gd.EventsCodeGenerator(project, layout, p);
  const codeGen = gd.EventsCodeGenerator.generateEventsCode(project, layout, layout.getEvents(), 'TestEvents.js', true);
  console.log('CodeGen success! Generated length:', codeGen.length);
});
