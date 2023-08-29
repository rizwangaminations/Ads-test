echo build.number=${bamboo.buildNumber} > $1
echo build.version.code=${bamboo.buildVersionCode} >> $1
echo build.commit.number=${bamboo.planRepository.revision} >> $1
echo build.branch.name=${bamboo.planRepository.branchName} >> $1
echo build.engine.version=${bamboo.engineVersion} >> $1