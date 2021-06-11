class Skill:
    @staticmethod
    def getSkillAtLevel(skill,level):
        return skill

    @staticmethod
    def getSkills(ship):
        """
        :param ship: Ship object
        :returns: 2d array of skills
        """
        out = []
        for skill in ship.ship["skill_ids"]:
            out += [Skill.getSkillAtLevel(skill,10)]
        return out
