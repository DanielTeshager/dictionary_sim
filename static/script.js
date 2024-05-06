// Utility functions
function scheduleHighlight(selector, color, delay) {
	setTimeout(function () {
		highlightBorder(selector, color);
	}, delay);
}

function highlightText(selector, textToHighlight) {
	$(selector).html(function (_, html) {
		const pattern = new RegExp(`(${textToHighlight})`, "gi");
		return html.replace(pattern, '<span class="highlight">$1</span>');
	});
}

function highlightBorder(selector, color) {
	$(selector)
		.css("border", "2px solid #" + color)
		.addClass("highlight-border");

	setTimeout(function () {
		$(selector).removeClass("highlight-border");
	}, 2000);
}

// AJAX requests
function simulateDictionary(dictString) {
	$.post("/simulate", { dict_string: dictString }, function (response) {
		updateSimulation(response);
		console.log(response);
	});
}

function lookupKey(dictString) {
	var randomColor = Math.floor(Math.random() * 16777215).toString(16);

	$.post("/lookup", { dict_string: dictString }, function (response) {
		console.log(response);
		if (response.error == true) {
			alert(response.message);
			return;
		}
		if (dictString == "") {
			alert("Can't do much with empty");
			return;
		}

		var delay = 0;
		var increment = 500;

		var hash_selector = ".box span:contains(" + response.hash_val + ")";
		scheduleHighlight(hash_selector, randomColor, (delay += increment));

		var indexSelector = "#dk-index-" + response.slot;
		scheduleHighlight(indexSelector, randomColor, (delay += increment));

		var entrySelector = "#dk-entry-" + response.slot;
		scheduleHighlight(entrySelector, randomColor, (delay += increment));

		var memSelector = ".memory-ref:contains(" + response.valRef + ")";
		scheduleHighlight(memSelector, randomColor, (delay += increment));

		var selector = ".ref-" + response.slot;
		var textToHighlight = response.valRef;
		setTimeout(function () {
			highlightText(selector, textToHighlight);
			$(selector).addClass("pulse");
		}, (delay += increment));

		var valSelector = $(memSelector).children()[1];
		var valText = valSelector.innerHTML;
		var value = valText.split(" ")[1];
		setTimeout(function () {
			highlightText(valSelector, value);
			$(valSelector).addClass("pulse");
		}, (delay += increment));

		currentText = $("#dict-input");
		setTimeout(() => {
			currentText.val(currentText.val() + ":" + value);
		}, (delay += increment));
	});
}

function deleteKey(key) {
	var randomColor = Math.floor(Math.random() * 16777215).toString(16);

	$.post("/delete", { dict_string: key }, function (response) {
		console.log(response);

		if (response.error == true) {
			alert(response.message);
			return;
		}

		if (key == "") {
			alert("Can't do much with empty");
			return;
		}

		var delay = 0;
		var increment = 500;

		var hash_selector = ".box span:contains(" + response.hash_val + ")";
		scheduleHighlight(hash_selector, randomColor, (delay += increment));

		var indexSelector = "#dk-index-" + response.slot;
		scheduleHighlight(indexSelector, randomColor, (delay += increment));

		var entrySelector = "#dk-entry-" + response.slot;
		scheduleHighlight(entrySelector, randomColor, (delay += increment));

		var memSelector = ".memory-ref:contains(" + response.valRef + ")";
		var memSelectorKey = ".memory-ref:contains(" + key + ")";
		scheduleHighlight(memSelector, randomColor, (delay += increment));

		var selector = ".ref-" + response.slot;
		var textToHighlight = response.valRef;
		setTimeout(function () {
			highlightText(selector, textToHighlight);
			$(selector).addClass("pulse");
		}, (delay += increment));

		var valSelector = $(memSelector).children()[1];
		var valText = valSelector.innerHTML;
		var value = valText.split(" ")[1];
		setTimeout(function () {
			highlightText(valSelector, value);
			$(valSelector).addClass("pulse");
		}, (delay += increment));

		setTimeout(function () {
			$(hash_selector).fadeOut(1000, function () {
				$(this).empty().show();
			});
			$(indexSelector).fadeOut(1000, function () {
				$(this).empty().show();
			});
			$(entrySelector).fadeOut(1000, function () {
				$(this).empty().show();
			});
			$(memSelector).fadeOut(1000, function () {
				$(this).empty().show();
			});
			$(memSelectorKey).fadeOut(1000, function () {
				$(this).empty().show();
			});
		}, delay + 500);
	});
}

// Update simulation functions
function updateHashingSection(data, animationDelay) {
	$("#key-hashing").empty();
	data.hashing.forEach(function (item, index) {
		var $hashBox = $('<div class="box"></div>');
		$hashBox.append("<span>" + item.key + "</span>");
		$hashBox.append('<span class="arrow">&#8594;</span>');
		$hashBox.append("<span>" + item.hash + "</span>");
		$hashBox
			.hide()
			.appendTo("#key-hashing")
			.delay(index * animationDelay)
			.fadeIn();
	});
}

function updateModuloCalculationSection(data, animationDelay) {
	$("#modulo-calculation").empty();
	data.modulo.forEach(function (item, index) {
		var $moduloBox = $('<div class="box"></div>');
		$moduloBox.append("<span>" + item.hash + "%" + item.dk_size + "</span>");
		$moduloBox.append('<span class="arrow">&#8594;</span>');
		$moduloBox.append("<span>Slot " + item.slot + "</span>");
		if (item.quadraticProbing) {
			$moduloBox.append(
				"<br><span>Quadratic Probing or Open Addressing</span>"
			);
		}
		$moduloBox
			.hide()
			.appendTo("#modulo-calculation")
			.delay(index * animationDelay)
			.fadeIn();
	});
}

function updateDkIndicesSection(data, animationDelay) {
	$("#dk-indices .slot-content").empty().removeClass("collision");
	data.dkIndices.forEach(function (item, index) {
		var $slotContent = $("#dk-index-" + item.slot + " .slot-content");
		$slotContent
			.hide()
			.text(item.hash)
			.delay(index * animationDelay)
			.fadeIn();
	});
}

function updateDkEntriesSection(data, animationDelay) {
	$("#dk-entries .slot-content").empty().removeClass("collision");
	data.dkEntries.forEach(function (item, index) {
		var $slotContent = $("#dk-entry-" + item.slot + " .slot-content");
		var content =
			"Hash: " +
			item.hashVal +
			"<br>" +
			"Key Ref: " +
			item.keyRef +
			"<br>" +
			"<span class=ref-" +
			item.slot +
			">Value Ref: " +
			item.valRef +
			"</span>";
		$slotContent
			.hide()
			.html(content)
			.delay(index * animationDelay)
			.fadeIn();
	});
}

function updateMemoryReferencesSection(data, animationDelay) {
	$("#memory-references").empty();
	data.memoryReferences.forEach(function (item, index) {
		var $memoryRef = $('<div class="memory-ref"></div>');
		var content =
			"Address: " +
			item.address +
			"<br>" +
			"<span class=val>Value: " +
			item.value +
			"</span>";
		$memoryRef
			.hide()
			.html(content)
			.appendTo("#memory-references")
			.delay(index * animationDelay)
			.fadeIn();
	});
}

function updateSimulation(data, animationDelay) {
	updateHashingSection(data, animationDelay);
	updateModuloCalculationSection(data, animationDelay);
	updateDkIndicesSection(data, animationDelay);
	updateDkEntriesSection(data, animationDelay);
	updateMemoryReferencesSection(data, animationDelay);
}

// AJAX requests
function simulateDictionary(dictString) {
	$.post("/simulate", { dict_string: dictString }, function (response) {
		var animationDelay = 1000;
		updateSimulation(response, animationDelay);
		console.log(response);
	});
}

// Event handlers
function handleSubmitButtonClick() {
	var dictString = $("#dict-input").val();
	if (dictString) {
		simulateDictionary(dictString);
	}
}

function handleLookupButtonClick() {
	var dictString = $("#dict-input").val();
	lookupKey(dictString);
}

function handleDeleteButtonClick() {
	var key = $("#dict-input").val();
	deleteKey(key);
}

// Document ready
$(document).ready(function () {
	var animationDelay = 1000;

	$("#submit-btn").click(handleSubmitButtonClick);
	$("#lookup-btn").click(handleLookupButtonClick);
	$("#delete-btn").click(handleDeleteButtonClick);
});
