$(document).ready(function () {
	  GetLatestReleaseInfo();
  });
  function GetLatestReleaseInfo() {
	  $.getJSON("https://api.github.com/repos/cedrick-f/pySequence/releases/latest").done(function (release) {
		var asset = release.assets[0];
		var downloadURL = "https://github.com/cedrick-f/pySequence/releases/download/" + release.tag_name + "/" + asset.name;
		$(".zip_win_download_link").attr("href", downloadURL);
		if (release.assets.length > 1) {
		  var asset = release.assets[1];
		  var downloadURL = "https://github.com/cedrick-f/pySequence/releases/download/" + release.tag_name + "/" + asset.name;
		  $(".exe_win_download_link").attr("href", downloadURL);
		}
		
		var downloadCount = 0;
		for (var i = 0; i < release.assets.length; i++) {
			downloadCount += release.assets[i].download_count;
		}
		var releaseInfo = release.name + "   -   mis à jour " + $.timeago(asset.updated_at) + "   -   téléchargé " + downloadCount + " fois";
		
		$(".release-info").text(releaseInfo);
		$(".release-info").fadeIn("slow");
	  });
  }