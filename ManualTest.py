import AttackSkill as AS
import DefenseSkill as DS
import SkillTree


perk1 = DS.Recover([[5]])
perk1.level_up()
skilltree1 = SkillTree.SkillTree([DS.DefenseSkill([perk1])])


perk1 = DS.Base([[0.5]])
perk1.level_up()
skilltree2 = SkillTree.SkillTree([DS.DefenseSkill([perk1])])