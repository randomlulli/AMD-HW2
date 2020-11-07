s = {'accessories.bag',
 'accessories.umbrella',
 'accessories.wallet',
 'apparel.belt',
 'apparel.costume',
 'apparel.dress',
 'apparel.jacket',
 'apparel.jeans',
 'apparel.scarf',
 'apparel.shirt',
 'apparel.shoes',
 'apparel.shoes.ballet_shoes',
 'apparel.shoes.espadrilles',
 'apparel.shoes.keds',
 'apparel.shoes.moccasins',
 'apparel.shoes.sandals',
 'apparel.shoes.slipons',
 'apparel.shoes.step_ins',
 'apparel.shorts',
 'apparel.skirt',
 'apparel.sock',
 'apparel.trousers',
 'apparel.tshirt',
 'apparel.underwear',
 'appliances.environment.air_conditioner',
 'appliances.environment.air_heater',
 'appliances.environment.fan',
 'appliances.environment.vacuum',
 'appliances.environment.water_heater',
 'appliances.iron',
 'appliances.ironing_board',
 'appliances.kitchen.blender',
 'appliances.kitchen.coffee_grinder',
 'appliances.kitchen.coffee_machine',
 'appliances.kitchen.dishwasher',
 'appliances.kitchen.grill',
 'appliances.kitchen.hob',
 'appliances.kitchen.hood',
 'appliances.kitchen.juicer',
 'appliances.kitchen.kettle',
 'appliances.kitchen.meat_grinder',
 'appliances.kitchen.microwave',
 'appliances.kitchen.mixer',
 'appliances.kitchen.oven',
 'appliances.kitchen.refrigerators',
 'appliances.kitchen.steam_cooker',
 'appliances.kitchen.toster',
 'appliances.kitchen.washer',
 'appliances.personal.hair_cutter',
 'appliances.personal.massager',
 'appliances.personal.scales',
 'appliances.sewing_machine',
 'auto.accessories.alarm',
 'auto.accessories.compressor',
 'auto.accessories.parktronic',
 'auto.accessories.player',
 'auto.accessories.radar',
 'auto.accessories.videoregister',
 'auto.accessories.winch',
 'computers.components.cooler',
 'computers.components.cpu',
 'computers.components.hdd',
 'computers.components.memory',
 'computers.components.motherboard',
 'computers.components.power_supply',
 'computers.components.videocards',
 'computers.desktop',
 'computers.ebooks',
 'computers.notebook',
 'computers.peripherals.camera',
 'computers.peripherals.keyboard',
 'computers.peripherals.monitor',
 'computers.peripherals.mouse',
 'computers.peripherals.printer',
 'construction.components.faucet',
 'construction.tools.drill',
 'construction.tools.generator',
 'construction.tools.light',
 'construction.tools.painting',
 'construction.tools.pump',
 'construction.tools.saw',
 'construction.tools.welding',
 'country_yard.cultivator',
 'country_yard.furniture.bench',
 'country_yard.furniture.hammok',
 'country_yard.lawn_mower',
 'electronics.audio.acoustic',
 'electronics.audio.headphone',
 'electronics.audio.microphone',
 'electronics.audio.music_tools.piano',
 'electronics.audio.subwoofer',
 'electronics.camera.photo',
 'electronics.camera.video',
 'electronics.clocks',
 'electronics.smartphone',
 'electronics.tablet',
 'electronics.telephone',
 'electronics.video.projector',
 'electronics.video.tv',
 'furniture.bathroom.bath',
 'furniture.bathroom.toilet',
 'furniture.bedroom.bed',
 'furniture.bedroom.blanket',
 'furniture.bedroom.pillow',
 'furniture.kitchen.chair',
 'furniture.kitchen.table',
 'furniture.living_room.cabinet',
 'furniture.living_room.chair',
 'furniture.living_room.sofa',
 'furniture.universal.light',
 'kids.carriage',
 'kids.dolls',
 'kids.fmcg.diapers',
 'kids.skates',
 'kids.swing',
 'kids.toys',
 'medicine.tools.tonometer',
 'sport.bicycle',
 'sport.ski',
 'sport.snowboard',
 'sport.tennis',
 'sport.trainer',
 'stationery.cartrige',}


l = list(elem.split('.') for elem in s)

category = dict()

#amz is a category root

for e in l:
    for i in range(len(e)):
        if i == 0 and e[i] not in category.keys():
            category[e[i]] = 'amz'
        elif e[i] not in category.keys():
            category[e[i]] = e[i-1]