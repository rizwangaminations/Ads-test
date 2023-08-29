db = connect('ds139277.mlab.com:39277/heroku_bvbpd2w5');
db.auth('heroku_bvbpd2w5', '5idsjjrpv9n576u9bps2ebqsp1');

printjson(db.stats());

var count = 0;

db.fs.files.find().forEach(removeFromChunkIfNotInDatabase);

db.repairDatabase();

printjson(db.stats());

quit();

function removeFromChunkIfNotInDatabase(chunk)
{

	print("file name = " + chunk.filename);
	
	//Look for the parent file in IAPPromo
	var iAPSDCol = db.IAPPromo.find({'Assets_SD' : chunk.filename}).count();
	var iAPHDCol = db.IAPPromo.find({'Assets_HD' : chunk.filename}).count();
	var iAPHDRCol = db.IAPPromo.find({'Assets_HDR' : chunk.filename}).count();
	
	//Look for the parent file in LEVELS
	var levelButtonHDCol = db.Levels.find({'LevelButton_HD' : chunk.filename}).count();
	var levelButtonHDRCol = db.Levels.find({'LevelButton_HDR' : chunk.filename}).count();
	var levelButtonSDCol = db.Levels.find({'LevelButton_SD' : chunk.filename}).count();
	var sfx_android = db.Levels.find({'sfx_android' : chunk.filename}).count();
	var sfx_ios = db.Levels.find({'sfx_ios' : chunk.filename}).count();
	var sfx_windows_phone = db.Levels.find({'sfx_windows_phone' : chunk.filename}).count();
	var jackpot_json = db.Levels.find({'jackpot_json' : chunk.filename}).count();
	var levelBundleHD = db.Levels.find({'LevelBundle_HD' : chunk.filename}).count();
	var levelBundleHDR = db.Levels.find({'LevelBundle_HDR' : chunk.filename}).count();
	var levelBundleSD = db.Levels.find({'LevelBundle_SD' : chunk.filename}).count();
	var levelBundleCommon = db.Levels.find({'LevelBundle_Common' : chunk.filename}).count();
	var levelButtonsPartsHDR = db.Levels.find({'LevelButtonParts_HDR' : chunk.filename}).count();
	var levelButtonsPartsHD = db.Levels.find({'LevelButtonParts_HD' : chunk.filename}).count();
	var levelButtonsPartsSD = db.Levels.find({'LevelButtonParts_SD' : chunk.filename}).count();
	var bonusBundleCommon = db.Levels.find({'BonusBundle_Common' : chunk.filename}).count();
	var bonusBundleHDR = db.Levels.find({'BonusBundle_HDR' : chunk.filename}).count();
	var bonusBundleHD = db.Levels.find({'BonusBundle_HD' : chunk.filename}).count();
	var bonusBundleSD = db.Levels.find({'BonusBundle_SD' : chunk.filename}).count();
	var bonus_sfx_ios = db.Levels.find({'Bonus_sfx_ios' : chunk.filename}).count();
	var bonus_sfx_android = db.Levels.find({'Bonus_sfx_android' : chunk.filename}).count();
	var bonus_sfx_windows_phone = db.Levels.find({'Bonus_sfx_windows_phone' : chunk.filename}).count();

	//Look for this parent files in MainMenuBonus
	var bonusBundleCommonMMB = db.MainMenuBonus.find({'BonusBundle_Common' : chunk.filename}).count();
	var bonusBundleHDRMMB = db.MainMenuBonus.find({'BonusBundle_HDR' : chunk.filename}).count();
	var bonusBundleHDMMB = db.MainMenuBonus.find({'BonusBundle_HD' : chunk.filename}).count();
	var bonusBundleSDMMB = db.MainMenuBonus.find({'BonusBundle_SD' : chunk.filename}).count();
	var bonus_sfx_iosMMB = db.MainMenuBonus.find({'Bonus_sfx_ios' : chunk.filename}).count();
	var bonus_sfx_androidMMB = db.MainMenuBonus.find({'Bonus_sfx_android' : chunk.filename}).count();
	var bonus_sfx_windows_phoneMMB = db.MainMenuBonus.find({'Bonus_sfx_windows_phone' : chunk.filename}).count();

	if (iAPSDCol == 0 && iAPHDCol == 0 && iAPHDRCol == 0 
		&& levelButtonHDCol == 0 && levelButtonHDRCol == 0 && levelButtonSDCol == 0 
		&& sfx_android == 0 && sfx_ios == 0 && sfx_windows_phone == 0 && jackpot_json == 0 
		&& levelBundleHD == 0 && levelBundleHDR == 0 && levelBundleSD == 0 && levelBundleCommon == 0
		&& levelButtonsPartsHDR == 0 && levelButtonsPartsHD == 0 && levelButtonsPartsSD == 0
		&& bonusBundleCommon == 0 && bonusBundleHDR == 0 && bonusBundleHD == 0 && bonusBundleSD == 0
		&& bonus_sfx_ios == 0 && bonus_sfx_android == 0 && bonus_sfx_windows_phone == 0
		&& bonusBundleCommonMMB == 0 && bonusBundleHDRMMB == 0 && bonusBundleHDMMB == 0 && bonusBundleSDMMB == 0 
		&& bonus_sfx_iosMMB == 0 && bonus_sfx_androidMMB == 0 && bonus_sfx_windows_phoneMMB == 0)
	{
		print("File not found in IAP or Level or MainMenuBonus table so delete it");

		status = db.fs.chunks.remove({'files_id': chunk._id});
		print("Deleted from fs.chunk" + status);
		status = db.fs.files.remove({'filename': chunk.filename});
		print("Deleted from fs.files" + status);
	}
	else
	{
		count += 1;
		print("found in IAP or Level or MainMenuBonus table don't delete " + count);
	}
}

