function watchDriveFolder() {
  var folderId = 'YOUR_FOLDER_ID'; // Replace with your Google Drive folder ID
  var folder = DriveApp.getFolderById(folderId);
  var files = folder.getFiles();

  while (files.hasNext()) {
    var file = files.next();
    if (file.getName() === 'resume.pdf') {
      var lastUpdated = file.getLastUpdated();
      var scriptProperties = PropertiesService.getScriptProperties();
      var lastTriggered = scriptProperties.getProperty('lastTriggered');

      if (!lastTriggered || new Date(lastTriggered) < lastUpdated) {
        triggerGitHubAction();
        scriptProperties.setProperty('lastTriggered', new Date().toISOString());
      }
    }
  }
}

function triggerGitHubAction() {
  var githubRepo = 'YOUR_USERNAME/YOUR_REPONAME'; // Replace with your GitHub username and repository name
  var githubToken = 'YOUR_GITHUB_TOKEN'; // Replace with your GitHub Personal Access Token

  var url = 'https://api.github.com/repos/' + githubRepo + '/dispatches';
  var payload = {
    'event_type': 'update-portfolio'
  };

  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'headers': {
      'Authorization': 'token ' + githubToken,
      'Accept': 'application/vnd.github.v3+json'
    },
    'payload': JSON.stringify(payload)
  };

  UrlFetchApp.fetch(url, options);
}

function createTimeDrivenTrigger() {
  ScriptApp.newTrigger('watchDriveFolder')
      .timeBased()
      .everyMinutes(5) // You can adjust the frequency
      .create();
}
