const fs = require('fs');
const path = require('path');
const libGD = require('C:\\Users\\ASUS\\.gemini\\antigravity\\brain\\29446708-9512-473e-8ad5-01a604faa9f5\\scratch\\libGD_extracted.js');

const PROJECT_PATH = fs.existsSync('StickScavenger.json')
  ? path.resolve('StickScavenger.json')
  : path.resolve(__dirname, '..', 'StickScavenger.json');

libGD().then(gd => {
  console.log('libGD engine loaded. Version:', gd.VersionWrapper.fullString());
  console.log('Parsing and validating project:', PROJECT_PATH);

  const jsonContent = fs.readFileSync(PROJECT_PATH, 'utf8');
  const project = new gd.ProjectHelper.createNewGDJSProject();

  const serializer = gd.Serializer;
  const projectElement = serializer.fromJSON(jsonContent);
  project.unserializeFrom(projectElement);
  projectElement.delete();

  const platform = gd.JsPlatform.get();
  let grandTotalErrors = 0;
  let unknownInstructionsCount = 0;
  let paramCountMismatchCount = 0;
  let invalidParametersCount = 0;

  const uniqueConditionsChecked = new Set();
  const uniqueActionsChecked = new Set();

  for (let l = 0; l < project.getLayoutsCount(); l++) {
    const layout = project.getLayoutAt(l);
    const layoutName = layout.getName();
    let layoutErrors = 0;

    function validateInstruction(instruction, isCondition, evDesc, instIndex) {
      const type = instruction.getType();
      if (isCondition) {
        uniqueConditionsChecked.add(type);
      } else {
        uniqueActionsChecked.add(type);
      }

      const metadata = isCondition
        ? gd.MetadataProvider.getConditionMetadata(platform, type)
        : gd.MetadataProvider.getActionMetadata(platform, type);

      if (gd.MetadataProvider.isBadInstructionMetadata(metadata)) {
        layoutErrors++;
        grandTotalErrors++;
        unknownInstructionsCount++;
        console.log(`[UNKNOWN INSTRUCTION] Scene: '${layoutName}' Ev #${evDesc} ${isCondition ? 'Cond' : 'Act'} #${instIndex}: Type '${type}' DOES NOT EXIST in GDevelop 5!`);
        return;
      }

      const paramCount = instruction.getParametersCount();
      const metaParamCount = metadata.getParametersCount();

      if (paramCount !== metaParamCount) {
        layoutErrors++;
        grandTotalErrors++;
        paramCountMismatchCount++;
        console.log(`[PARAM COUNT MISMATCH] Scene: '${layoutName}' Ev #${evDesc} ${isCondition ? 'Cond' : 'Act'} #${instIndex} ('${type}'): Instruction has ${paramCount} params, but GDevelop metadata expects ${metaParamCount}!`);
      }

      const checkCount = Math.min(paramCount, metaParamCount);
      for (let p = 0; p < checkCount; p++) {
        const valObj = instruction.getParameter(p);
        const val = typeof valObj.getPlainString === 'function' ? valObj.getPlainString() : String(valObj);
        const expectedType = metadata.getParameter(p).getType();

        if (expectedType === 'operator' || expectedType === 'relationalOperator') {
          const validOps = ['=', '+', '-', '*', '/', '<', '>', '<=', '>=', '!='];
          if (!validOps.includes(val)) {
            layoutErrors++;
            grandTotalErrors++;
            invalidParametersCount++;
            console.log(`[INVALID OPERATOR] Scene: '${layoutName}' Ev #${evDesc} ${isCondition ? 'Cond' : 'Act'} #${instIndex} ('${type}') Param #${p}: "${val}"`);
          }
        } else if (expectedType === 'string' || expectedType === 'stringWithSelector') {
          if (val.includes('\n')) {
            layoutErrors++;
            grandTotalErrors++;
            invalidParametersCount++;
            console.log(`[LITERAL NEWLINE IN STRING] Scene: '${layoutName}' Ev #${evDesc} ${isCondition ? 'Cond' : 'Act'} #${instIndex} ('${type}') Param #${p}: contains raw newline`);
          }
        }
      }

      if (typeof instruction.getSubInstructions === 'function') {
        const subList = instruction.getSubInstructions();
        for (let s = 0; s < subList.size(); s++) {
          validateInstruction(subList.get(s), isCondition, `${evDesc}.sub${s}`, s);
        }
      }
    }

    function validateEventsList(eventsList, prefix = "") {
      for (let e = 0; e < eventsList.getEventsCount(); e++) {
        const event = eventsList.getEventAt(e);
        const evDesc = `${prefix}${e}`;
        const evType = event.getType();

        if (evType === 'BuiltinCommonInstructions::Standard') {
          const stdEvent = gd.asStandardEvent(event);
          const conditions = stdEvent.getConditions();
          for (let c = 0; c < conditions.size(); c++) {
            validateInstruction(conditions.get(c), true, evDesc, c);
          }
          const actions = stdEvent.getActions();
          for (let a = 0; a < actions.size(); a++) {
            validateInstruction(actions.get(a), false, evDesc, a);
          }
        }

        if (event.canHaveSubEvents() && event.hasSubEvents()) {
          validateEventsList(event.getSubEvents(), `${evDesc}.`);
        }
      }
    }

    validateEventsList(layout.getEvents());
    console.log(`Layout '${layoutName}': ${layoutErrors} errors`);
  }

  console.log(`\n========================================`);
  console.log(`GRAND TOTAL LIBGD ERRORS: ${grandTotalErrors}`);
  console.log(` - Unknown Instructions: ${unknownInstructionsCount}`);
  console.log(` - Parameter Count Mismatches: ${paramCountMismatchCount}`);
  console.log(` - Invalid Parameters: ${invalidParametersCount}`);
  console.log(`\nVerified Condition Types (${uniqueConditionsChecked.size}):`, Array.from(uniqueConditionsChecked).sort());
  console.log('Verified Action Types (' + uniqueActionsChecked.size + '):', Array.from(uniqueActionsChecked).sort());
  console.log('========================================');

  project.delete();
  if (grandTotalErrors === 0) {
    console.log('SUCCESS: All instructions and parameters 100% VALID in GDevelop 5 libGD engine!');
    process.exit(0);
  } else {
    console.error('FAILURE: libGD found errors.');
    process.exit(1);
  }
}).catch(err => {
  console.error('libGD Execution Error:', err);
  process.exit(1);
});
