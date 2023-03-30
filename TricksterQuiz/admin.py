from django.contrib import admin

#Import Models
from TricksterQuiz.models import Skill_Level_Quiz, Quiz_Section, Section_Trick, Term_Bonus, Bonus_Question, Bonus_Answer, Section_Result


@admin.register(Skill_Level_Quiz)
class QuizAdmin(admin.ModelAdmin):
  fields = ('QuizTitle', 'QuizDiscription', 'QuizNoOfSections', 'QuizImg')
  list_display = ('QuizTitle', 'QuizNoOfSections')
  ordering = ('QuizID',)
  search_fields = ('QuizTitle',)

@admin.register(Quiz_Section)
class SectionAdmin(admin.ModelAdmin):
  fields = ('SectionQuiz', 'SectionName', 'SectionDiscription', 'SectionNoOfQuestions', 'SectionLevel', 'SectionFailScore', 'SectionPassScore', 'SectionNumber', 'SectionImg')
  list_display = ('SectionName', 'SectionFailScore', 'SectionPassScore', 'SectionLevel')
  ordering = ('SectionQuiz', 'SectionNumber')
  search_fields = ('SectionQuiz', 'SectionName', 'SectionNumber')

@admin.register(Section_Trick)
class TrickSectionAdmin(admin.ModelAdmin):
  fields = ('Trick', 'TrickSection', 'TrickValue')
  list_display = ('Trick', 'TrickSection', 'TrickValue')
  ordering = ('TrickSection', 'TrickValue')
  search_fields = ('TrickSection', 'TrickValue')

@admin.register(Term_Bonus)
class TermBonusAdmin(admin.ModelAdmin):
  fields = ('BonusName', 'BonusSection', 'BonusNoOfTerms', 'BonusImg')
  list_display = ('BonusName', 'BonusSection', 'BonusNoOfTerms')
  ordering = ('BonusSection', 'BonusName')
  search_fields = ('TrickSection', 'TrickValue')

@admin.register(Section_Result)
class ResultAdmin(admin.ModelAdmin):
  fields = ('ResultSection', 'ResultBonus', 'ResultUser', 'TrickScore', 'BonusScore')
  list_display = ('ResultUser', 'TrickScore', 'BonusScore')
  ordering = ('ResultUser',)
  search_fields = ('ResultSection', 'ResultBonus', 'ResultUser')

class BonusAnswerInLine(admin.TabularInline):
  model = Bonus_Answer
  fieldsets = (
    ('Answer', {'fields': ('AnswerText', 'AnswerCorrect', 'AnswerQuestion')}),
  )

class BonusQuestionAdmin(admin.ModelAdmin):
  inlines = [BonusAnswerInLine]
  search_fields = ('QuestionTerm', 'QuestionSection')
  ordering = ('QuestionSection', 'QuestionNumber')
  list_display = ('QuestionTerm', 'QuestionSection', 'QuestionNumber')
  fieldsets = (
    ('Question', {'fields': ('QuestionText', 'QuestionSection', 'QuestionNumber', 'QuestionTerm', 'QuestionImg')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('QuestionText', 'QuestionSection', 'QuestionNumber', 'QuestionTerm', 'QuestionImg')}
    ),
  )

admin.site.register(Bonus_Question, BonusQuestionAdmin)