class Config:
    def __init__(self):
        # parameters for training
        self.num_epoch = 50
        self.batch_size = 8
        self.train_num_workers = 12  # number of threads to load data when training
        self.val_num_workers = 8
        self.num_pairs = 8
        self.threshold = 0.3        # parameter for checking out of boundary

        self.lr = 1e-3               # learning rate of SGD
        self.momentum = 0.9          # momentum of SGD
        self.weight_decay = 1e-4     # weight decay of optimizator
        self.step_size = 1           # step size of LR_Schedular
        self.gamma = 0.8685          # decay rate of LR_Schedular

        # path to your trained model
        self.net_base_path = "/app/models"
        self.net = "ResNet50_50_model_1e3.pth"

        # path to test image
        self.test_base_path = "/app/downloads"

        # parameters for test
        self.classes = 38
        self.label = [
                        "Anthurium_BacterialBlight",
                        "Anthurium_BacterialWilt",
                        "Anthurium_BlackNose",
                        "Anthurium_Healthy",
                        "Anthurium_PhytophthoraPythium",
                        "Anthurium_Rhizoctonia_RootRot",
                        "Crotons_Healthy",
                        "Crotons_MealyBugs",
                        "Crotons_ScaleInsects",
                        "DracaenaMarginata_Healthy",
                        "DracaenaMarginata_InsectPests",
                        "DracaenaMarginata_Soil",
                        "DracaenaMarginata_Temperature",
                        "GoldenPothos_BacterialLeafSpot",
                        "GoldenPothos_BacterialWilt",
                        "GoldenPothos_Healthy",
                        "GoldenPothos_PhytophthoraRootRot",
                        "LuckyBoomboo_BambooMites",
                        "LuckyBoomboo_Healthy",
                        "LuckyBoomboo_PowderyMildew",
                        "MothOrchid_BacterialBrownSpot",
                        "MothOrchid_BlackRot",
                        "MothOrchid_Botrytis",
                        "MothOrchid_Healthy",
                        "PeaceLily_Healthy",
                        "PeaceLily_InsectInfection",
                        "PeaceLily_LackOfWater",
                        "PeaceLily_Overwatering",
                        "PeaceLily_Sunburn",
                        "PonytailPalm_Bugs",
                        "PonytailPalm_Cylindrocladium",
                        "PonytailPalm_Healthy",
                        "SnakePlant_BrownSpots",
                        "SnakePlant_Healthy",
                        "SnakePlant_WaterOversupply",
                        "Syngonium_BacterialLeafBlight",
                        "Syngonium_BacterialStemRot",
                        "Syngonium_Healthy"
                    ]

        self.accuracy = [
                        "Anthurium_BacterialBlight_0",
                        "Anthurium_BacterialWilt_0",
                        "Anthurium_BlackNose_0",
                        "Anthurium_Healthy_89",
                        "Anthurium_PhytophthoraPythium_0",
                        "Anthurium_Rhizoctonia_RootRot_0",
                        "Crotons_Healthy_89",
                        "Crotons_MealyBugs_50",
                        "Crotons_ScaleInsects_60",
                        "DracaenaMarginata_Healthy_94",
                        "DracaenaMarginata_InsectPests_100",
                        "DracaenaMarginata_Soil_0",
                        "DracaenaMarginata_Temperature_0",
                        "GoldenPothos_BacterialLeafSpot_69",
                        "GoldenPothos_BacterialWilt_25",
                        "GoldenPothos_Healthy_96",
                        "GoldenPothos_PhytophthoraRootRot_0",
                        "LuckyBoomboo_BambooMites_0",
                        "LuckyBoomboo_Healthy_91",
                        "LuckyBoomboo_PowderyMildew_33",
                        "MothOrchid_BacterialBrownSpot_50",
                        "MothOrchid_BlackRot_100",
                        "MothOrchid_Botrytis_100",
                        "MothOrchid_Healthy_80",
                        "PeaceLily_Healthy_100",
                        "PeaceLily_InsectInfection_0",
                        "PeaceLily_LackOfWater_75",
                        "PeaceLily_Overwatering_0",
                        "PeaceLily_Sunburn_0",
                        "PonytailPalm_Bugs_100",
                        "PonytailPalm_Cylindrocladium_50",
                        "PonytailPalm_Healthy_72",
                        "SnakePlant_BrownSpots_16",
                        "SnakePlant_Healthy_90",
                        "SnakePlant_WaterOversupply_66",
                        "Syngonium_BacterialLeafBlight_100",
                        "Syngonium_BacterialStemRot_0",
                        "Syngonium_Healthy_92"
                    ]