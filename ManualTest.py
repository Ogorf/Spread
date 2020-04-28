import AttackSkill as AS
import DefenseSkill as DS
import PopulationSkill as PS
import SkillTree


perk1 = PS.Reinforcements([[60]])
perk1.level_up()
skilltree1 = SkillTree.SkillTree([PS.PopulationSkill([perk1])])


perk1 = AS.Berserker([(10, 0.1)])
skilltree2 = SkillTree.SkillTree([AS.AttackSkill([perk1])])
