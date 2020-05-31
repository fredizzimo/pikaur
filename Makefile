# This file is licensed under GPLv3, see https://www.gnu.org/licenses/

LANGS := fr ru pt de is tr da nl es zh_CN it ja

LOCALEDIR := locale
POTFILE := $(LOCALEDIR)/pikaur.pot
POFILES := $(addprefix $(LOCALEDIR)/,$(addsuffix .po,$(LANGS)))
POTEMPFILES := $(addprefix $(LOCALEDIR)/,$(addsuffix .po~,$(LANGS)))
MOFILES = $(POFILES:.po=.mo)

MAN_FILE := pikaur.1
MAN_FILE_BAK := pikaur.1.repo
MD_MAN_FILE := $(MAN_FILE).md

all: locale

locale: $(MOFILES)

$(POTFILE):
	# find pikaur -type f -name '*.py' -not -name 'argparse.py' \
		#
	find pikaur -type f -name '*.py' \
		| xargs xgettext --language=python --add-comments --sort-output \
			--default-domain=pikaur --from-code=UTF-8 --keyword='_n:1,2' --output=$@

$(LOCALEDIR)/%.po: $(POTFILE)
	test -f $@ || msginit --locale=$* --no-translator --input=$< --output=$@
	msgmerge --update $@ $<

%.mo: %.po
	msgfmt -o $@ $<

clean_man:
	$(RM) $(MD_MAN_FILE)

clean: clean_man clean_checkman
	$(RM) $(LANGS_MO)
	$(RM) $(POTEMPFILES)

man: clean_man
	cp README.md $(MD_MAN_FILE)
	sed -i \
		-e 's/^##### /### /g' \
		-e 's/^#### /### /g' \
		$(MD_MAN_FILE)
	ronn $(MD_MAN_FILE) --manual="Pikaur manual" -r
	sed -i \
		-e '/travis/d' \
		-e '/Screenshot/d' \
		-e 's/\(^\.SS.*\)\\"\(.*\)\\"/\1'"'"'\2'"'"'/g' \
		$(MAN_FILE)

backup_man:
	mv $(MAN_FILE) $(MAN_FILE_BAK)

_check_man: backup_man man
	tail -n +5 $(MAN_FILE) > $(MAN_FILE).compare
	tail -n +5 $(MAN_FILE_BAK) > $(MAN_FILE_BAK).compare
	mv $(MAN_FILE_BAK) $(MAN_FILE)
	diff $(MAN_FILE).compare $(MAN_FILE_BAK).compare

clean_checkman:
	$(RM) $(MAN_FILE_BAK).compare
	$(RM) $(MAN_FILE).compare

check_man: _check_man clean_checkman

.PHONY: all clean $(POTFILE) clean_man man backup_man check_man clean_checkman
.PRECIOUS: $(LOCALEDIR)/%.po
