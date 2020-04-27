import AttackSkill as AS
import DefenseSkill as DS
import SkillTree


perk1 = DS.Recover([[5]])
perk1.level_up()
skilltree1 = SkillTree.SkillTree([DS.DefenseSkill([perk1])])


perk1 = AS.Berserker([(10, 0.1)])
perk1.level_up()
skilltree2 = SkillTree.SkillTree([AS.AttackSkill([perk1])])
