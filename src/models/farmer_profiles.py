from typing import Dict, List
from .data_models import FarmerProfile, EducationLevel, IncomeLevel

class FarmerProfileManager:
    """Manager for farmer profiles and personas"""
    
    def __init__(self, farmer_personas_config: Dict):
        self.personas_config = farmer_personas_config
        self.sample_farmers = self._load_sample_farmers()
    
    def _load_sample_farmers(self) -> List[FarmerProfile]:
        """Load sample farmers from config"""
        farmers = []
        
        for farmer_data in self.personas_config.get("sample_farmers", []):
            farmer = FarmerProfile(
                id=farmer_data.get("id", f"F{len(farmers)+1:03d}"),
                name=farmer_data["name"],
                age=farmer_data["age"],
                education=EducationLevel(farmer_data["education"]),
                income=IncomeLevel(farmer_data["income"]),
                location=farmer_data["location"],
                crops=farmer_data["crops"],
                land_size=farmer_data["land_size"],
                skepticism=farmer_data["skepticism"],
                govt_experience=farmer_data["govt_experience"],
                family_size=farmer_data["family_size"],
                persona_type=farmer_data.get("persona_type")
            )
            farmers.append(farmer)
        
        return farmers
    
    def get_farmer_by_id(self, farmer_id: str) -> FarmerProfile:
        """Get farmer by ID"""
        for farmer in self.sample_farmers:
            if farmer.id == farmer_id:
                return farmer
        raise ValueError(f"Farmer with ID {farmer_id} not found")
    
    def get_farmers_by_education(self, education: EducationLevel) -> List[FarmerProfile]:
        """Get farmers by education level"""
        return [f for f in self.sample_farmers if f.education == education]
    
    def get_farmers_by_skepticism(self, min_skepticism: float = 0.0, max_skepticism: float = 1.0) -> List[FarmerProfile]:
        """Get farmers by skepticism range"""
        return [f for f in self.sample_farmers 
                if min_skepticism <= f.skepticism <= max_skepticism]
    
    def get_persona_template(self, persona_type: str) -> Dict:
        """Get persona template by type"""
        templates = self.personas_config.get("persona_templates", {})
        if persona_type not in templates:
            raise ValueError(f"Persona type {persona_type} not found")
        return templates[persona_type]
    
    def create_custom_farmer(self, **kwargs) -> FarmerProfile:
        """Create a custom farmer profile"""
        required_fields = ["name", "age", "education", "income", "location", 
                          "crops", "land_size", "skepticism", "govt_experience", "family_size"]
        
        for field in required_fields:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")
        
        # Convert string enums to enum types
        if isinstance(kwargs["education"], str):
            kwargs["education"] = EducationLevel(kwargs["education"])
        if isinstance(kwargs["income"], str):
            kwargs["income"] = IncomeLevel(kwargs["income"])
        
        # Generate ID if not provided
        if "id" not in kwargs:
            kwargs["id"] = f"FC{len(self.sample_farmers)+1:03d}"
        
        return FarmerProfile(**kwargs)